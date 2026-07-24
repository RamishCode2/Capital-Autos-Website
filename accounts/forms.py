from django import forms
from django.contrib.auth.forms import SetPasswordForm


class PasswordResetSetPasswordForm(SetPasswordForm):
    """Keeps Django's password validators with customer-friendly labels."""

    new_password1 = forms.CharField(
        label="New Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )
    new_password2 = forms.CharField(
        label="Confirm Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )
