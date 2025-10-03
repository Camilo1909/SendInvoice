from django import forms

from .models import TypeInvoice


class InvoiceForm(forms.Form):
    phone_number = forms.CharField(
        label="Número de teléfono", widget=forms.TextInput(attrs={"class": "form-control"})
    )
    type = forms.ModelChoiceField(
        queryset=TypeInvoice.objects.all(),
        label="Concepto de la factura",
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    img_invoice = forms.ImageField(
        label="Imagen de la factura",
        widget=forms.ClearableFileInput(
            attrs={"class": "form-control d-none", "id": "invoice-image"}
        ),
    )
