from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from escrow.models import Escrow
from .forms import RatingForm
from .models import Reviews

@login_required
def leave_rating(request, escrow_id):
    escrow = get_object_or_404(Escrow, id=escrow_id)

    if escrow.status != "COMPLETED":
        return redirect("escrow_status", escrow_id=escrow.id)

    if request.user == escrow.buyer:
        role = "BUYER"
        target = escrow.seller
    elif request.user == escrow.seller:
        role = "SELLER"
        target = escrow.buyer
    else:
        return redirect("/")

    if Rating.objects.filter(escrow=escrow, role=role).exists():
        return redirect("escrow_status", escrow_id=escrow.id)

    if request.method == "POST":
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.escrow = escrow
            rating.given_by = request.user
            rating.given_to = target
            rating.role = role
            rating.save()
            return redirect("escrow_status", escrow_id=escrow.id)
    else:
        form = RatingForm()

    return render(request, "ratings/leave.html", {
        "form": form,
        "target": target,
        "role": role
    })
