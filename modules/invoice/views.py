from django.contrib import messages
from django.shortcuts import redirect, render

from core.decorators import owner_or_role_required
from modules.auths.models import Account
from modules.base.models import Client
from modules.services.models import WhatsAppService

from .forms import InvoiceForm, SendInvoiceForm
from .models import Invoice

# Create your views here.


@owner_or_role_required("Admin")
def invoice_list(request):
    invoices = Invoice.objects.all()
    return render(request, "invoice_list.html", {"invoices": invoices})


@owner_or_role_required("Admin")
def invoice_query(request, invoice_id):
    try:
        invoice = Invoice.objects.get(pk=invoice_id)
    except Invoice.DoesNotExist:
        messages.error(request, "Factura no existente")

    form = InvoiceForm(instance=invoice)
    for field in form.fields.values():
        field.widget.attrs["readonly"] = True
        field.widget.attrs["disabled"] = True
    return render(request, "invoice_query.html", {"form": form})


@owner_or_role_required("Admin")
def send_invoice(request):
    account = Account.getAccount(request.user)
    if request.method == "POST":
        form = SendInvoiceForm(request.POST, request.FILES)
        if form.is_valid():
            phone_number = form.cleaned_data["phone_number"]
            img_invoice = form.cleaned_data["img_invoice"]
            type = form.cleaned_data["type"]

            try:
                client = Client.objects.get(phone_number=phone_number)
            except Client.DoesNotExist:
                client = Client(phone_number=phone_number, created_by=account.username)
                client.save()
            invoice = Invoice(
                client=client, img_invoice=img_invoice, type=type, created_by=account.username
            )

            def send_whatsapp_hook():
                WhatsAppService.send_invoice(
                    phone_number=invoice.client.phone_number, image_url=invoice.img_invoice
                )

            invoice.on_saved = send_whatsapp_hook
            invoice.save()

        else:
            print(form.errors)
    else:
        form = SendInvoiceForm()

    return render(request, "send_invoice.html", {"form": form})


@owner_or_role_required("Admin")
def resend_invoice(request, invoice_id):
    try:
        invoice = Invoice.objects.get(id=invoice_id)
    except Invoice.DoesNotExist:
        messages.error("Invoice not found")
        return redirect("invoice_list")
    WhatsAppService.send_invoice(
        phone_number=invoice.client.phone_number, image_url=invoice.img_invoice
    )
    messages.success(request, "Factura reenviada exitosamente.")
    return redirect("invoice_list")
