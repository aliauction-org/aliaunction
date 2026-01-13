from django import forms
from .models import Dispute

class DisputeForm(forms.ModelForm):
    class Meta:
        model = Dispute
        fields = ["issue_type", "description"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }
