from django.shortcuts import render


def home(request):

    return render(request, "layouts/home.html")
