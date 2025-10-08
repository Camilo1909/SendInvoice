from django.db import IntegrityError, transaction
from django.core.files.base import ContentFile
from django.db.models.functions import Cast
from django.db.models import DateField
from django.db.models import Func
from django.utils import timezone
from django.db import models
from io import BytesIO
from PIL import Image
import os

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
    function = 'DATE'
    template = "DATE(timezone('America/Bogota', %(expressions)s))"

class Invoice(models.Model):
    client = models.ForeignKey(Client, verbose_name="Cliente", null=False, on_delete=models.PROTECT)
    code = models.CharField(verbose_name="Codigo", unique=True, blank=True)
    img_invoice = models.ImageField(upload_to="invoices/", verbose_name="Imagen de la factura", blank=False)
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
    
    @staticmethod
    def resize_for_whatsapp(image_file, filename, layout="square", quality=85):
        """
        Resize an image according to WhatsApp Business API recommended dimensions.

        Args:
            image_file: Django UploadedFile or ImageField file
            filename: Base name for the new image file (string)
            layout: 'square' (1080x1080) or 'horizontal' (1200x628)
            quality: JPEG compression quality (1-100)

        Returns:
            Django ContentFile ready to save into ImageField
        """
        dimensions = {"square": (1080, 1080), "horizontal": (1200, 628)}

        if layout not in dimensions:
            raise ValueError("layout must be 'square' or 'horizontal'")

        img = Image.open(image_file)

        # Convert to RGB if it has transparency
        if img.mode in ("RGBA", "LA", "P"):
            background = Image.new("RGB", img.size, (255, 255, 255))
            if img.mode == "P":
                img = img.convert("RGBA")
            background.paste(img, mask=img.split()[-1] if img.mode == "RGBA" else None)
            img = background

        target_width, target_height = dimensions[layout]
        original_ratio = img.width / img.height
        target_ratio = target_width / target_height

        if original_ratio > target_ratio:
            new_width = target_width
            new_height = int(target_width / original_ratio)
        else:
            new_height = target_height
            new_width = int(target_height * original_ratio)

        resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # White canvas centered
        final_img = Image.new("RGB", (target_width, target_height), (255, 255, 255))
        offset_x = (target_width - new_width) // 2
        offset_y = (target_height - new_height) // 2
        final_img.paste(resized_img, (offset_x, offset_y))

        buffer = BytesIO()
        final_img.save(buffer, format="JPEG", quality=quality, optimize=True)
        buffer.seek(0)

        new_name = f"{filename}.jpg"
        return ContentFile(buffer.read(), name=new_name)

    def save(self, *args, **kwargs):
        if not self.code:
            local_today = timezone.localdate()  # Fecha local actual
            
            # Contar facturas del cliente creadas hoy (en hora local)
            count = (
                Invoice.objects
                .filter(client=self.client)
                .annotate(local_date=ToLocalDate('created_at'))
                .filter(local_date=local_today)
                .count() + 1
            )

            # Generar código único
            self.code = f"{self.client.phone_number}{local_today.strftime('%Y%m%d')}{count:03d}"

            # Intentar guardar, en caso de colisión repetir
            for attempt in range(5):
                try:
                    super().save(*args, **kwargs)
                    return
                except IntegrityError:
                    count += 1
                    self.code = f"{self.client.phone_number}{local_today.strftime('%Y%m%d')}{count:03d}"

            raise IntegrityError("No se pudo generar un código único tras varios intentos.")
        else:
            super().save(*args, **kwargs)
        if self.img_invoice:
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
