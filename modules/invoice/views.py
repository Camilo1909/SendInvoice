from modules.auths.models import Account
from modules.base.models import Client
from django.shortcuts import render
from .forms import InvoiceForm
from .models import Invoice

# Create your views here.

def invoice_list(request):
    invoices = Invoice.objects.all()
    return render(request,"invoice_list.html", {"invoices":invoices} )

def sendInvoice(request):
    account = Account.getAccount(request.user)
    if request.method == 'POST':
        form =  InvoiceForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data["phone_number"]
            img_invoice = form.cleaned_data["img_invoice"]

            try:
                client =  Client.objects.get(phone_number= phone_number)
            except Client.DoesNotExist:
                cliente = Client(
                    phone_number = phone_number,
                    created_by = account.username
                )
                client.save()
            
            invoice = Invoice(
                client = client,
                img_invoice = img_invoice,
                created_by = account.username
            )
    else:
        form = InvoiceForm()

    return render(request, "send_invoice.html", {"form": form})        
            