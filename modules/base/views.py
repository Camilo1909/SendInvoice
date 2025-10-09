from django.shortcuts import render, redirect

from core.decorators import owner_or_role_required, owner_required

from .models import Client, Company

from django.contrib import messages

from .forms import ClientForm

from modules.auths.models import Account

# Create your views here.


@owner_or_role_required("Admin")
def client_list(request):
    clients = Client.objects.all()
    return render(request, "client/client_list.html", {"clients": clients})

@owner_or_role_required("Admin")
def client_update(request, client_id):
    account = Account.getAccount(request.user)
    try:
        client = Client.objects.get(id=client_id)
    except Client.DoesNotExist:
        client = None
        messages.error(request, "Client not found.")
        return render(request, "client/client_list.html")
    
    if request.method == "POST":
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            change = False
            if client.phone_number != form.cleaned_data['phone_number']:
                if Client.objects.filter(phone_number=form.cleaned_data['phone_number']).exists():
                    messages.error(request, "Phone number already exists.")
                    return render(request, "client/client_update.html", {"client": client, "form": form})
                else:
                    client.phone_number = form.cleaned_data['phone_number']
                    change = True
            if client.name != form.cleaned_data['name']:
                client.name = form.cleaned_data['name']
                change = True
            if client.last_names != form.cleaned_data['last_name']:
                client.last_names = form.cleaned_data['last_name']
                change = True
            if client.email != form.cleaned_data['email']:
                client.email = form.cleaned_data['email']
                change = True
            if change:
                client.updated_by = account.username
                client.save()
            messages.success(request, "Client updated successfully.")
            return redirect("client_list")
    else:
        form = ClientForm(instance=client)
    return render(request, "client/client_update.html", {"client": client})


@owner_required
def company_list(request):
    companies = Company.objects.all()
    return render(request, "company/company_list.html", {"companies": companies})
