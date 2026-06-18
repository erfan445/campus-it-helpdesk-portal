from django import forms
from .models import Asset


class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = [
            'asset_tag',
            'name',
            'category',
            'status',
            'serial_number',
            'location',
            'assigned_to',
            'purchase_date',
            'warranty_expiry',
            'notes',
        ]
        widgets = {
            'purchase_date': forms.DateInput(attrs={'type': 'date'}),
            'warranty_expiry': forms.DateInput(attrs={'type': 'date'}),
        }
