from django.contrib import messages
from django.core.paginator import Paginator
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
    paginator = Paginator(invoices, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "invoice_list.html", {"page_obj": page_obj})


@owner_or_role_required("Admin")
def invoice_query(request, invoice_id):
    try:
        invoice = Invoice.objects.get(pk=invoice_id)
    except Invoice.DoesNotExist:
        messages.error(request, "Factura no existente")

    image_url = None
    if invoice.img_invoice:
        key = f"media/{invoice.img_invoice.name}"  # "media/invoices/factura.png"
        image_url = WhatsAppService.generate_presigned_url(key)

    form = InvoiceForm(instance=invoice)
    for field in form.fields.values():
        field.widget.attrs["readonly"] = True
        field.widget.attrs["disabled"] = True
    return render(request, "invoice_query.html", {"form": form, "image_url": image_url})


@owner_or_role_required("Admin")
def send_invoice(request):
    account = Account.getAccount(request.user)
    if request.method == "POST":
        form = SendInvoiceForm(request.POST, request.FILES)
        if form.is_valid():
            phone_number = form.cleaned_data["phone_number"]
            if len(phone_number) != 10:
                messages.error(request, "El número de teléfono debe tener 10 dígitos.")
                return render(request, "send_invoice.html", {"form": form})
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
            invoice.save()
            messages.success(request, "Factura enviada exitosamente.")
            redirect("sendInvoice")
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
    image_input = invoice.img_invoice.url if invoice.img_invoice else None
    try:
        sent = WhatsAppService.send_invoice(
            phone_number=invoice.client.phone_number, image_url=image_input
        )
    except Exception as e:
        print(f"[Error] No se pudo reenviar la factura: {e}")
        messages.error(request, f"No se pudo reenviar la factura: {e}")
        return redirect("invoice_list")
    if sent:
        messages.success(request, "Factura reenviada exitosamente.")
    else:
        messages.error(request, "Error al reenviar la factura.")
    return redirect("invoice_list")
