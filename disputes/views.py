from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from auctions.models import Auction
from .models import Dispute
from .forms import DisputeForm

@login_required
def raise_dispute(request, auction_id):
    auction = get_object_or_404(Auction, id=auction_id)

    if request.method == "POST":
        form = DisputeForm(request.POST)
        if form.is_valid():
            dispute = form.save(commit=False)
            dispute.raised_by = request.user
            dispute.auction = auction
            dispute.save()
            return redirect("my_disputes")
    else:
        form = DisputeForm()

    return render(request, "disputes/raise.html", {
        "form": form,
        "auction": auction
    })


@login_required
def my_disputes(request):
    disputes = Dispute.objects.filter(raised_by=request.user)
    return render(request, "disputes/my_disputes.html", {
        "disputes": disputes
    })
