from django import forms
from .models import Order


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order

        fields = [
            "full_name",
            "phone",
            "email",
            "address",
            "city",
            "payment_method",
        ]

        widgets = {
            "full_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Full Name"
            }),

            "phone": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "03XXXXXXXXX"
            }),

            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "Email (Optional)"
            }),

            "address": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Delivery Address"
            }),

            "city": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "City"
            }),

            "payment_method": forms.Select(attrs={
                "class": "form-select"
            }),
        }