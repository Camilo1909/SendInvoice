from django.db.models.signals import post_save
from django.dispatch import receiver

from modules.services.models import WhatsAppService

from .models import Invoice


@receiver(post_save, sender=Invoice)
def send_invoice_whatsapp(sender, instance, created, **kwargs):
    """
    Se ejecuta después de guardar un Invoice.
    Cuando se crea, envía la imagen al número del cliente por WhatsApp.
    """
    if created and instance.img_invoice:
        try:
            image_url = instance.img_invoice.url  # ✅ URL pública en S3
            print(f"[Signal] Enviando factura {instance.id} a {instance.client.phone_number}")
            WhatsAppService.send_invoice(
                phone_number=instance.client.phone_number,
                image_url=image_url,
            )
        except Exception as e:
            print(f"[Signal Error] No se pudo enviar WhatsApp para invoice {instance.id}: {e}")
