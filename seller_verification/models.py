from django.db import models
from users.models import User

class SellerVerification(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="seller_verification"
    )

    phone_number = models.CharField(max_length=15)
    address = models.TextField()

    phone_verified = models.BooleanField(default=False)
    admin_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def is_verified(self):
        return self.phone_verified and self.admin_verified

    def __str__(self):
        return f"{self.user.username} verification"
