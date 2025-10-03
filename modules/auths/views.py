from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from core.decorators import owner_required

from .forms import LoginForm
from .models import Account

# Create your views here.


def logout_app(request):
    logout(request)
    return redirect("home")


def login_app(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is None:
                msg = "Error en las credenciales"
                messages.error(request, msg)
            else:
                account = Account.getAccount(user)
                login(request, user)
                msg = f"Bienvenido {account.get_full_name}"
                return redirect("sendInvoice")
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})


@owner_required
def users_list(request):
    users = Account.objects.all()
    return render(request, "user_list.html", {"users": users})
