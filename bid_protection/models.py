from django.db import models
from users.models import User

class UserStatus(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_suspended = models.BooleanField(default=False)
    reason = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def _str_(self):
        return f"{self.user.username} - {'Suspended' if self.is_suspended else 'Active'}"
