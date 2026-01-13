from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import PlatformPaymentDetails, UserPaymentProfile, PaymentProof
from .forms import UserPaymentProfileForm, PaymentProofForm
from auctions.models import Auction
from .models import Invoice, payment

# Create your views here.

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
        payment = Payment.objects.create(
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
