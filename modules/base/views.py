from django.shortcuts import render
from .models import Client

# Create your views here.

def client_list(request):
    clients = Client.objects.all()
    return render(request,"client_list.html", {"clients":clients} )
