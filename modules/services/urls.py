from django.urls import path

from . import views  # suponiendo que crees un módulo 'whatsapp'

urlpatterns = [
    path("webhook/whatsapp/", views.whatsapp_webhook, name="whatsapp_webhook"),
]
