from django.shortcuts import render

from modules.auths.models import Account


def home(request):
    user = Account.getAccount(request.user)

    return render(request, "layouts/home.html", {"user": user})
