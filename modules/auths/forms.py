from django import forms
from django.contrib.auth.forms import SetPasswordForm

from .models import Account


class LoginForm(forms.Form):
    username = forms.CharField(
        label="Usuario",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Usuario"}),
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Contraseña"}),
    )


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "rol",
            "company",
        ]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control"}),
            "rol": forms.SelectMultiple(attrs={"class": "form-select"}),
            "company": forms.Select(attrs={"class": "form-select"}),
        }


class AccountPasswordForm(SetPasswordForm):
    """
    Usa el mismo SetPasswordForm de Django, pero con estilos personalizados.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["new_password1"].widget.attrs.update({"class": "form-control"})
        self.fields["new_password2"].widget.attrs.update({"class": "form-control"})
