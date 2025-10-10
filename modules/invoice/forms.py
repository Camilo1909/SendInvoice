from django import forms

from .models import Invoice, TypeInvoice


class SendInvoiceForm(forms.Form):
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
            attrs={"class": "form-control visually-hidden", "id": "invoice-image"}
        ),
    )


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ["code", "client", "type", "img_invoice"]
        widgets = {
            "code": forms.TextInput(attrs={"class": "form-control"}),
            "client": forms.Select(attrs={"class": "form-select"}),
            "type": forms.Select(attrs={"class": "form-select"}),
            "img_invoice": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }
