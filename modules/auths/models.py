from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

# Create your models here.

class Role(models.Model):
    id = models.IntegerField(verbose_name="ID", primary_key=True)
    name = models.CharField(verbose_name="Nombre")
    description = models.CharField(verbose_name="Descripcion")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Rol"
        verbose_name_plural = "Roles"
        ordering = ["name"]
        app_label = "auths"

class StatusAccount(models.Model):
    id = models.IntegerField(verbose_name="ID", primary_key=True)
    name = models.CharField(verbose_name="Nombre")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Estado de la cuenta"
        verbose_name_plural = "Estados de la cuenta"
        ordering = ["name"]
        app_label = "auths"

class Account(AbstractUser):
    phone_number = models.CharField(verbose_name="Numero de telefono")
    status = models.ForeignKey(StatusAccount, verbose_name="Estado", on_delete=models.PROTECT)
    roles = models.ForeignKey(Role, verbose_name="Rol", on_delete=models.PROTECT)

    groups = models.ManyToManyField(
        Group,
        related_name="accounts",  # <- nombre único para tu modelo
        blank=True,
        verbose_name="grupos"
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="accounts_permissions",  # <- nombre único para tu modelo
        blank=True,
        verbose_name="permisos de usuario"
    )

    @staticmethod
    def getAccount(user):
        if type(user) == str:
            username = user
        else:
            username = user.username
        
        try:
            account = Account.objects.get(username = username)
        except:
            account = None
        
        return account

    @property
    def fullname(self):
        return self.get_full_name()
    
    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Cuenta de usuario"
        verbose_name_plural = "Cuentas de usuario"
        ordering = ["id"]
        app_label = "auths"