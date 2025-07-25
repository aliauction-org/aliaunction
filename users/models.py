from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    # Additional fields can be added here if needed
    # Bid and purchase history will be related via ForeignKey/ManyToMany from auctions
    pass
