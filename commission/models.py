from django.db import models

class CommissionRule(models.Model):
    seller_percent = models.DecimalField(max_digits=5, decimal_places=2, default=10.00)
    buyer_percent = models.DecimalField(max_digits=5, decimal_places=2, default=3.00)

    transport_note = models.TextField(
        default="Transport charges are paid by Buyer directly to Seller"
    )

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Active Commission Rule"
