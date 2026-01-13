from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from escrow.models import Escrow
from .models import ShippingDetail
from .forms import ShippingForm

@login_required
def add_shipping(request, escrow_id):
    escrow = get_object_or_404(Escrow, id=escrow_id, buyer=request.user)

    shipping, created = ShippingDetail.objects.get_or_create(escrow=escrow)

    if request.method == "POST":
        form = ShippingForm(request.POST, instance=shipping)
        if form.is_valid():
            form.save()
            return redirect("escrow_status", escrow_id=escrow.id)
    else:
        form = ShippingForm(instance=shipping)

    return render(request, "shipping/form.html", {
        "form": form,
        "escrow": escrow
    })
