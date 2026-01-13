from django import forms

class AuctionSearchForm(forms.Form):
    q = forms.CharField(
        required=False,
        label="Search",
        widget=forms.TextInput(attrs={"placeholder": "Search auctions..."})
    )
    min_price = forms.DecimalField(required=False, min_value=0)
    max_price = forms.DecimalField(required=False, min_value=0)
    live_only = forms.BooleanField(required=False)
    ending_soon = forms.BooleanField(required=False)
    newest = forms.BooleanField(required=False)
