from django.contrib import admin

from .models import Invoice, TypeInvoice

# Register your models here.
admin.site.register(Invoice)
admin.site.register(TypeInvoice)
