from django.db import models

# Create your models here.

class Company(models.Model):
    name = models.CharField(verbose_name="Nombre",blank=False)
    short_name = models.CharField(verbose_name="Nombre corto",blank=False)
    email = models.EmailField(verbose_name="Correo electronico", blank=False)
    address = models.CharField(verbose_name="Direccion", blank=False)

    created_by = models.CharField(verbose_name="Creado por")
    created_at = models.DateTimeField(verbose_name="Fecha de creacion", auto_now_add=True)
    updated_by = models.CharField(verbose_name="Actualizado por", blank=True, null=True)
    updated_at = models.DateTimeField(verbose_name="Fecha de actualizacion", auto_now_add=True)

    def __str__(self):
        return self.short_name
    
    @property
    def get_admins(self):
        return self.accounts.filter(rol__name__iexact='Admin')

    class Meta:
        verbose_name = "Compañia"
        verbose_name_plural = "Compañias"
        ordering = ["name"]
        app_label = "base"


class Client (models.Model):
    name = models.CharField(verbose_name="Nombre",blank=True)
    last_names = models.CharField(verbose_name="Apellidos", blank=True)
    email = models.EmailField(verbose_name="Correo electronico", blank=True)
    phone_number = models.CharField(verbose_name="Numero de celular",unique=True)

    created_by = models.CharField(verbose_name="Creado por")
    created_at = models.DateTimeField(verbose_name="Fecha de creacion", auto_now_add=True)
    updated_by = models.CharField(verbose_name="Actualizado por", blank=True, null=True)
    updated_at = models.DateTimeField(verbose_name="Fecha de actualizacion", auto_now_add=True)

    def __str__(self):
        return self.phone_number

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ["-created_at"]
        app_label = "base"
