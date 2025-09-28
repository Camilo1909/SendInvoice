from modules.auths.models import Account
from modules.auths.models import Role
from django.db import models

# Create your models here.

class MenuItem(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre")
    url = models.CharField(max_length=200, verbose_name="URL")
    roles = models.ManyToManyField(Role, verbose_name="Roles", blank=True) 
    order = models.PositiveIntegerField(verbose_name="Ordén", default=0)  # Para ordenar los items
    is_active = models.BooleanField(default=True)  # Para desactivar sin eliminar

    @classmethod
    def get_items_for_user(cls, request):
        account = Account.getAccount(request.user)
        items = cls.objects.filter(is_active=True)
        
        if account and account.is_authenticated:
            user_roles = account.roles.all()  # Suponiendo que user.roles es ManyToManyField
            items = items.filter(models.Q(roles__in=user_roles) | models.Q(roles__isnull=True)).distinct()
        else:
            # Solo items públicos
            items = items.filter(roles__isnull=True)
        
        return items

    class Meta:
        ordering = ['order']
        app_label = "menu"

    def __str__(self):
        return self.name