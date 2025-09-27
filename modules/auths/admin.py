from django.contrib import admin
from .models import Account, Role, StatusAccount

# Register your models here.
admin.site.register(Account)
admin.site.register(Role)
admin.site.register(StatusAccount)
