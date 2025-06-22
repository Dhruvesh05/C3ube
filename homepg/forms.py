# forms.py
from django import forms
from .models import Stock

class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['category', 'name', 'price', 'image']


class BillForm(forms.Form):
    bill_items = forms.CharField(widget=forms.HiddenInput())
    total_amount = forms.DecimalField(widget=forms.HiddenInput())