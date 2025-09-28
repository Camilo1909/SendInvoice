from modules.auths.models import Account
from django.shortcuts import render

def home(request):
    user = Account.getAccount(request.user)

    return render(request, 'layouts/home.html',{
        "user": user
    })