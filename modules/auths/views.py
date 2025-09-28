from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import LoginForm
from .models import Account

# Create your views here.

def login_app(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username = form.cleaned_data["username"],
                password = form.cleaned_data["password"]
            )
            if user is None:
                msg = "Error en las credenciales"
                messages.error(request, msg)
            else:
                account = Account.getAccount(user)
                login(request, user)
                msg = f"Bienvenido {account.get_full_name}"
                return redirect('sendInvoice')
    else:
        form = LoginForm()
    return render(request, 'login.html', {"form":form})