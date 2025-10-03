from modules.auths.models import Account
from modules.auths.models import Role
from django.db import models

# Create your models here.

class MenuItem(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre")
    url = models.CharField(max_length=200, verbose_name="URL")
    roles = models.ManyToManyField(Role, verbose_name="Roles", blank=True)
    icon = models.CharField(max_length=100, verbose_name="Icono", blank=True, null=True) 
    order = models.PositiveIntegerField(verbose_name="Ordén", default=0)  # Para ordenar los items
    is_active = models.BooleanField(default=True)  # Para desactivar sin eliminar

    @classmethod
    def get_items_for_user(cls, request):
        """
        Devuelve los ítems de menú visibles para el usuario autenticado y su rol.
        """
        items = cls.objects.filter(is_active=True)

        account = Account.getAccount(request.user) if request.user.is_authenticated else None
        
        if account:
            user_roles = account.rol.all()
            items = items.filter(
                models.Q(roles__in=user_roles) | models.Q(roles__isnull=True)
            ).distinct()
        else:
            # Solo ítems públicos (sin roles asignados)
            items = items.filter(roles__isnull=True)

        return items.order_by("order")

    class Meta:
        ordering = ['order']
        app_label = "menu"

    def __str__(self):
        return self.name