from django.urls import path

from . import views

urlpatterns = [
    path("sendInvoice/", views.sendInvoice, name="sendInvoice"),
    path("resendInvoice/<int:invoice_id>/", views.resendInvoice, name="resendInvoice"),
    path("invoices/", views.invoice_list, name="invoice_list"),
]
