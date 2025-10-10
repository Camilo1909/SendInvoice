import os

from django.conf import settings
from django.db import IntegrityError, models
from django.db.models import Func
from django.utils import timezone

from PIL import Image

from modules.base.models import Client


class TypeInvoice(models.Model):
    id = models.IntegerField(verbose_name="ID", primary_key=True)
    name = models.CharField(verbose_name="Nombre")
    description = models.CharField(verbose_name="Descripcion")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Concepto de Factura"
        verbose_name_plural = "Conceptos de Factura"
        ordering = ["name"]
        app_label = "invoice"


class ToLocalDate(Func):
    function = "DATE"
    template = "DATE(timezone('America/Bogota', %(expressions)s))"


class Invoice(models.Model):
    client = models.ForeignKey(Client, verbose_name="Cliente", null=False, on_delete=models.PROTECT)
    code = models.CharField(verbose_name="Codigo", unique=True, blank=True)
    img_invoice = models.ImageField(
        upload_to="invoices/", verbose_name="Imagen de la factura", blank=False
    )
    type = models.ForeignKey(
        TypeInvoice,
        verbose_name="Concepto de la factura",
        null=False,
        blank=False,
        on_delete=models.PROTECT,
    )

    created_by = models.CharField(verbose_name="Creado por")
    created_at = models.DateTimeField(verbose_name="Fecha de creacion", auto_now_add=True)
    updated_by = models.CharField(verbose_name="Actualizado por", blank=True, null=True)
    updated_at = models.DateTimeField(verbose_name="Fecha de actualizacion", auto_now_add=True)

    def __str__(self):
        return self.code

    def save(self, *args, **kwargs):
        if not self.code:
            local_today = timezone.localdate()  # Fecha local actual

            # Contar facturas del cliente creadas hoy (en hora local)
            count = (
                Invoice.objects.filter(client=self.client)
                .annotate(local_date=ToLocalDate("created_at"))
                .filter(local_date=local_today)
                .count()
                + 1
            )

            # Generar código único
            self.code = f"{self.client.phone_number}{local_today.strftime('%Y%m%d')}{count:03d}"

            # Intentar guardar, en caso de colisión repetir
            for attempt in range(100):
                try:
                    super().save(*args, **kwargs)
                    break
                except IntegrityError:
                    count += 1
                    self.code = (
                        f"{self.client.phone_number}{local_today.strftime('%Y%m%d')}{count:03d}"
                    )
        else:
            super().save(*args, **kwargs)
        if not getattr(settings, "USE_S3", False) and self.img_invoice:
            image_path = self.img_invoice.path
            img = Image.open(image_path)

            # Convertir a RGB si tiene transparencia
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            # Redimensionar (ejemplo: cuadrada para WhatsApp)
            img = img.resize((1080, 1080), Image.Resampling.LANCZOS)

            new_filename = f"{self.code}.jpg"
            new_path = os.path.join(os.path.dirname(image_path), new_filename)

            img.save(new_path, "JPEG", quality=85, optimize=True)

            if self.img_invoice.name != f"invoices/{new_filename}":
                self.img_invoice.name = f"invoices/{new_filename}"
                super().save(update_fields=["img_invoice"])

    class Meta:
        verbose_name = "Factura"
        verbose_name_plural = "Facturas"
        ordering = ["-created_at"]
        app_label = "invoice"
