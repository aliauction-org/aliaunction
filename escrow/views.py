from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Escrow
from .services import mark_shipped, mark_delivered

@login_required
def mark_shipped_view(request, escrow_id):
    escrow = get_object_or_404(Escrow, id=escrow_id, seller=request.user)
    mark_shipped(escrow)
    return redirect("escrow_status", escrow_id=escrow.id)

@login_required
def mark_delivered_view(request, escrow_id):
    escrow = get_object_or_404(Escrow, id=escrow_id, buyer=request.user)
    mark_delivered(escrow)
    return redirect("escrow_status", escrow_id=escrow.id)
