from django import forms
from .models import Review, Rating

class ReviewRatingForm(forms.Form):
    score = forms.IntegerField(min_value=1, max_value=5, label='Rating (1-5)')
    content = forms.CharField(widget=forms.Textarea, label='Review') 