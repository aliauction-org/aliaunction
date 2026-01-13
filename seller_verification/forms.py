from django import forms
from .models import SellerVerification

class SellerVerificationForm(forms.ModelForm):
    class Meta:
        model = SellerVerification
        fields = ["phone_number", "address"]


class OTPForm(forms.Form):
    otp = forms.CharField(max_length=6)
