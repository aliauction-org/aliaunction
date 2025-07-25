from django import forms
from .models import PlatformPaymentDetails, UserPaymentProfile, PaymentProof

class PlatformPaymentDetailsForm(forms.ModelForm):
    class Meta:
        model = PlatformPaymentDetails
        fields = ['bank_name', 'account_number', 'ifsc_code', 'account_holder_name', 'upi_id', 'qr_code', 'additional_instructions']

class UserPaymentProfileForm(forms.ModelForm):
    class Meta:
        model = UserPaymentProfile
        fields = ['bank_name', 'account_number', 'ifsc_code', 'account_holder_name', 'upi_id', 'qr_code', 'additional_instructions']

class PaymentProofForm(forms.ModelForm):
    class Meta:
        model = PaymentProof
        fields = ['screenshot', 'comments'] 