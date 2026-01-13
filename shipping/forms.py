from django import forms
from .models import ShippingDetail

class ShippingForm(forms.ModelForm):
    class Meta:
        model = ShippingDetail
        exclude = ("escrow", "delivery_charge")
