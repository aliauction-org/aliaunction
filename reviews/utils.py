from django.db.models import Avg
from .models import Rating

def get_reputation(user):
    return Rating.objects.filter(given_to=user).aggregate(
        avg=Avg("stars")
    )["avg"] or 0
