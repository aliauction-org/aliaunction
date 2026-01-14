"""
Escrow service functions for status updates.
"""
from django.utils import timezone


def mark_shipped(escrow):
    """Mark escrow status as SHIPPED by seller."""
    if escrow.status == 'PAID':
        escrow.status = 'SHIPPED'
        escrow.last_updated = timezone.now()
        escrow.save()
        return True
    return False


def mark_delivered(escrow):
    """Mark escrow status as DELIVERED by buyer."""
    if escrow.status == 'SHIPPED':
        escrow.status = 'DELIVERED'
        escrow.last_updated = timezone.now()
        escrow.save()
        
        # Automatically mark as COMPLETED after delivery confirmation
        escrow.status = 'COMPLETED'
        escrow.save()
        return True
    return False


def mark_paid(escrow):
    """Mark escrow status as PAID after payment confirmation."""
    if escrow.status == 'PENDING_PAYMENT':
        escrow.status = 'PAID'
        escrow.last_updated = timezone.now()
        escrow.save()
        return True
    return False
