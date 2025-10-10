from django.urls import path

from . import views

urlpatterns = [
    path("sendInvoice/", views.send_invoice, name="sendInvoice"),
    path("resendInvoice/<int:invoice_id>/", views.resend_invoice, name="resend_invoice"),
    path("invoices/", views.invoice_list, name="invoice_list"),
    path("invoices/query/<int:invoice_id>/", views.invoice_query, name="invoice_query"),
]
