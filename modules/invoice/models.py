from modules.base.models import Client
from django.db import models
from django.utils import timezone

class Invoice(models.Model):
    client = models.ForeignKey(Client, verbose_name="Cliente", null=False, on_delete=models.PROTECT)
    code = models.CharField(verbose_name="Codigo",unique=True, blank=True)
    img_invoice = models.ImageField(verbose_name="Imagen de la factura", blank=False)

    created_by = models.CharField(verbose_name="Creado por")
    created_at = models.DateTimeField(verbose_name="Fecha de creacion", auto_now_add=True)
    updated_by = models.CharField(verbose_name="Actualizado por")
    updated_at = models.DateTimeField(verbose_name="Fecha de actualizacion", auto_now_add=True)

    def __str__(self):
        return self.code

    def save(self, *args, **kwargs):
        if not self.code:
            today = timezone.now().date()
            count = Invoice.objects.filter(client=self.client, created_at=today).count() + 1
            self.code = f"{self.client.phone_number}{today.strftime('%Y%m%d')}{count:03d}"
        super.save(*args, **kwargs)

    class Meta:
        verbose_name = "Factura"
        verbose_name_plural = "Facturas"
        ordering = ["-created_at"]
        app_label = "invoice"
