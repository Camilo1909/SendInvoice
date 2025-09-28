from django.urls import path
from . import views

urlpatterns = [
    path("sendInvoice/", views.sendInvoice, name="sendInvoice")
]