from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import PlatformPaymentDetails, UserPaymentProfile, PaymentProof
from .forms import UserPaymentProfileForm, PaymentProofForm
from auctions.models import Auction
from .models import Invoice, InvoicePayment
from django.http import HttpResponse
from django.template.loader import render_to_string

# Try to import WeasyPrint, but make it optional
try:
    from weasyprint import HTML
    WEASYPRINT_AVAILABLE = True
except OSError:
    # WeasyPrint requires external libraries (gobject, pango, etc.)
    WEASYPRINT_AVAILABLE = False
    HTML = None

@login_required
def payment_profile(request):
    profile, created = UserPaymentProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserPaymentProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Payment profile updated successfully!')
            return redirect('payment_profile')
    else:
        form = UserPaymentProfileForm(instance=profile)
    return render(request, 'payments/payment_profile.html', {'form': form})

@login_required
def upload_payment_proof(request, auction_id):
    auction = get_object_or_404(Auction, id=auction_id)
    if request.method == 'POST':
        form = PaymentProofForm(request.POST, request.FILES)
        if form.is_valid():
            payment_proof = form.save(commit=False)
            payment_proof.auction = auction
            payment_proof.payer = request.user
            payment_proof.payee = auction.owner  # Platform will be handled differently
            payment_proof.amount = auction.current_price
            payment_proof.direction = 'to_platform'
            payment_proof.save()
            messages.success(request, 'Payment proof uploaded successfully!')
            return redirect('auction_detail', auction_id=auction.id)
    else:
        form = PaymentProofForm()
    return render(request, 'payments/upload_payment_proof.html', {'form': form, 'auction': auction})

@login_required
def confirm_payment_received(request, payment_proof_id):
    payment_proof = get_object_or_404(PaymentProof, id=payment_proof_id, payee=request.user)
    if request.method == 'POST':
        payment_proof.status = 'verified'
        payment_proof.save()
        messages.success(request, 'Payment confirmed!')
    return redirect('payment_history')

@login_required
def payment_history(request):
    payments_made = PaymentProof.objects.filter(payer=request.user).order_by('-created_at')
    payments_received = PaymentProof.objects.filter(payee=request.user).order_by('-created_at')
    return render(request, 'payments/payment_history.html', {
        'payments_made': payments_made,
        'payments_received': payments_received
    })

def platform_payment_details(request):
    try:
        platform_details = PlatformPaymentDetails.objects.first()
    except PlatformPaymentDetails.DoesNotExist:
        platform_details = None
    return render(request, 'payments/platform_payment_details.html', {'platform_details': platform_details})

@login_required
def invoice_view(request, auction_id):
    invoice = get_object_or_404(Invoice, auction__id=auction_id, buyer=request.user)
    return render(request, "payments/invoice.html", {"invoice": invoice})


@login_required
def pay_invoice(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id, buyer=request.user)

    if request.method == "POST":
        method = request.POST.get("method")
        payment = InvoicePayment.objects.create(
            invoice=invoice,
            method=method,
            status="SUCCESS"  # simulate success
        )
        
        if hasattr(invoice.auction, "escrow") and hasattr(invoice.auction.escrow, "shipping"):
            invoice.transport_charge = invoice.auction.escrow.shipping.delivery_charge
            invoice.save(update_fields=["transport_charge"])
    
        invoice.status = "PAID"
        invoice.save()
        return redirect("invoice_view", auction_id=invoice.auction.id)

    return render(request, "payments/pay.html", {"invoice": invoice})


@login_required
def download_invoice(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)

    if request.user not in [invoice.buyer, invoice.seller] and not request.user.is_staff:
        return HttpResponse("Unauthorized", status=403)

    html_string = render_to_string(
        "payments/invoice_pdf.html",
        {"invoice": invoice}
    )

    if WEASYPRINT_AVAILABLE and HTML:
        pdf = HTML(string=html_string).write_pdf()
        response = HttpResponse(pdf, content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="invoice_{invoice.id}.pdf"'
        return response
    else:
        # Fallback: return HTML if WeasyPrint not available
        return HttpResponse(html_string, content_type="text/html")


@login_required
def winner_checkout(request, auction_id):
    """
    Winner checkout flow - creates Invoice and Escrow for the auction winner.
    Only accessible by the winning bidder after auction ends.
    """
    from decimal import Decimal
    from escrow.models import Escrow
    from commission.models import CommissionRule
    
    auction = get_object_or_404(Auction, id=auction_id)
    
    # Verify auction has ended
    from django.utils import timezone
    if auction.end_time > timezone.now():
        messages.error(request, "This auction hasn't ended yet.")
        return redirect('auction_detail', auction_id=auction.id)
    
    # Get the winning bid
    highest_bid = auction.bids.order_by('-amount', '-timestamp').first()
    if not highest_bid:
        messages.error(request, "No bids were placed on this auction.")
        return redirect('auction_detail', auction_id=auction.id)
    
    # Verify current user is the winner
    if highest_bid.user != request.user:
        messages.error(request, "You are not the winner of this auction.")
        return redirect('auction_detail', auction_id=auction.id)
    
    # Check if invoice already exists
    try:
        invoice = Invoice.objects.get(auction=auction)
        return redirect('invoice_view', auction_id=auction.id)
    except Invoice.DoesNotExist:
        pass
    
    # Get commission rules
    try:
        commission_rule = CommissionRule.objects.filter(is_active=True).first()
        buyer_percent = commission_rule.buyer_percent if commission_rule else Decimal('3.00')
        seller_percent = commission_rule.seller_percent if commission_rule else Decimal('10.00')
    except CommissionRule.DoesNotExist:
        buyer_percent = Decimal('3.00')
        seller_percent = Decimal('10.00')
    
    # Calculate commissions
    amount = auction.current_price
    buyer_commission = (amount * buyer_percent / 100).quantize(Decimal('0.01'))
    seller_commission = (amount * seller_percent / 100).quantize(Decimal('0.01'))
    
    # Create Invoice
    invoice = Invoice.objects.create(
        auction=auction,
        buyer=request.user,
        seller=auction.owner,
        amount=amount,
        buyer_commission=buyer_commission,
        seller_commission=seller_commission,
        transport_charge=Decimal('0.00'),  # Set later with shipping
        status='PENDING'
    )
    
    # Create Escrow
    Escrow.objects.create(
        auction=auction,
        buyer=request.user,
        seller=auction.owner,
        status='PENDING_PAYMENT'
    )
    
    messages.success(request, 'Invoice created! Please proceed to payment.')
    return redirect('invoice_view', auction_id=auction.id)
