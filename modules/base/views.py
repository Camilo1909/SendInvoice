from django.contrib import messages
from django.shortcuts import redirect, render

from core.decorators import owner_or_role_required, owner_required
from modules.auths.models import Account

from .forms import ClientForm, CompanyForm
from .models import Client, Company

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
        return redirect("client_list")
    if request.method == "POST":
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            if (
                Client.objects.exclude(id=client.id)
                .filter(phone_number=form.cleaned_data["phone_number"])
                .exists()
            ):
                messages.error(request, "Phone number already exists.")
                return render(request, "client/client_update.html", {"form": form})

            client = form.save(commit=False)
            client.updated_by = account.username
            client.save()

            messages.success(request, "Client updated successfully.")
            return redirect("client_list")
    else:
        form = ClientForm(instance=client)
    return render(request, "client/client_update.html", {"form": form})


owner_or_role_required("Admin")


def client_query(request, client_id):
    try:
        client = Client.objects.get(id=client_id)
    except Client.DoesNotExist:
        client = None
        messages.error(request, "Client not found.")
        return redirect("client_list")
    form = ClientForm(instance=client)
    for field in form.fields.values():
        field.widget.attrs["readonly"] = True
        field.widget.attrs["disabled"] = True
    return render(request, "client/client_query.html", {"form": form})


@owner_required
def company_list(request):
    companies = Company.objects.all()
    return render(request, "company/company_list.html", {"companies": companies})


@owner_required
def company_create(request):
    account = Account.getAccount(request.user)
    if request.method == "POST":
        form = CompanyForm(request.POST)
        if form.is_valid():
            company = form.save(commit=False)
            company.created_by = account.username
            company.save()
            messages.success(request, "Compañia creada exitosamente.")
            return redirect("company_list")
    else:
        form = CompanyForm()
    return render(request, "company/company_create.html", {"form": form})


@owner_required
def company_update(request, company_id):
    account = Account.getAccount(request.user)
    try:
        company = Company.objects.get(id=company_id)
    except Company.DoesNotExist:
        company = None
        messages.error(request, "Compañia no encontrada.")
        return redirect("company_list")
    if request.method == "POST":
        form = CompanyForm(request.POST, instance=company)
        if form.is_valid():
            company = form.save(commit=False)
            company.updated_by = account.username
            company.save()
            messages.success(request, "Compañia actualizada exitosamente.")
            return redirect("company_list")
    else:
        form = CompanyForm(instance=company)
    return render(request, "company/company_update.html", {"form": form})


@owner_required
def company_query(request, company_id):
    try:
        company = Company.objects.get(id=company_id)
    except Company.DoesNotExist:
        company = None
        messages.error(request, "Compañia no encontrada.")
        return redirect("company_list")
    form = CompanyForm(instance=company)
    for field in form.fields.values():
        field.widget.attrs["readonly"] = True
        field.widget.attrs["disabled"] = True
    return render(request, "company/company_query.html", {"form": form})
