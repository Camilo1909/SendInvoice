from django.urls import path
from . import views

urlpatterns= [
    path("clients/", views.client_list, name="client_list"),
    path("companies/", views.company_list, name="company_list")
]