from django import forms
from .models import Rating


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ["stars", "review"]
        widgets = {
            "stars": forms.NumberInput(attrs={"min": 1, "max": 5}),
            "review": forms.Textarea(attrs={"rows": 3}),
        }

