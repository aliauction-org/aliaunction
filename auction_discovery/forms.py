from django import forms
from auctions.models import Category


class AuctionSearchForm(forms.Form):
    q = forms.CharField(
        required=False,
        label="Search",
        widget=forms.TextInput(attrs={"placeholder": "Search auctions..."})
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.filter(is_active=True),
        required=False,
        empty_label="All Categories"
    )
    min_price = forms.DecimalField(required=False, min_value=0)
    max_price = forms.DecimalField(required=False, min_value=0)
    live_only = forms.BooleanField(required=False)
    ending_soon = forms.BooleanField(required=False)
    newest = forms.BooleanField(required=False)

