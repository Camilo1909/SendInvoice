from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Invoice
from modules.services.models import WhatsAppService

@receiver(post_save, sender=Invoice)
def send_invoice_whatsapp(sender, instance, created, **kwargs):
    """
    Se ejecuta después de guardar un Invoice.
    created=True indica que es un nuevo registro.
    """
    if created:
        print(f"Disparando WhatsApp para invoice {instance.id}")
        WhatsAppService.send_invoice(phone_number=instance.client.phone_number)
