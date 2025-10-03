from django.shortcuts import render
from .models import Client, Company
from core.decorators import owner_or_role_required, owner_required

# Create your views here.

@owner_or_role_required('Admin')
def client_list(request):
    clients = Client.objects.all()
    return render(request,"client/client_list.html", {"clients":clients} )

@owner_required
def company_list(request):
    companies = Company.objects.all()
    return render(request,"company/company_list.html", {"companies":companies} )
