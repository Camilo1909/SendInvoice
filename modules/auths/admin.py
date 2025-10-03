from .models import Account, Role, StatusAccount
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

# Register your models here.
@admin.register(Account)
class AccountAdmin(UserAdmin):
    # Campos que se mostrarán en la lista
    list_display = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'company', 'status', 'is_active', 'is_staff']
    list_filter = ['status', 'is_active', 'is_staff', 'rol', 'company']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'company__name']
    
    # Configuración de campos en el formulario de edición
    fieldsets = (
        ('Información de Usuario', {
            'fields': ('username', 'password')
        }),
        ('Información Personal', {
            'fields': ('first_name', 'last_name', 'email', 'phone_number')
        }),
        ('Compañía y Roles', {
            'fields': ('company', 'status', 'rol', 'is_active', 'is_staff', 'is_superuser')
        }),
        ('Fechas Importantes', {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',)  # Hace que esta sección esté colapsada por defecto
        }),
    )
    
    # Configuración de campos para crear un nuevo usuario
    add_fieldsets = (
        ('Credenciales', {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
        ('Información Personal', {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email', 'phone_number')
        }),
        ('Compañía y Configuración', {
            'classes': ('wide',),
            'fields': ('company', 'status', 'rol', 'is_active', 'is_staff')
        }),
    )
    
    # Campos que se pueden editar en la lista
    filter_horizontal = ('rol',)  # Hace más fácil seleccionar múltiples roles
    
    # Orden de los registros
    ordering = ['username']
    
    # Ocultar groups y user_permissions
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if 'groups' in form.base_fields:
            form.base_fields.pop('groups')
        if 'user_permissions' in form.base_fields:
            form.base_fields.pop('user_permissions')
        return form

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description']
    search_fields = ['name']
    list_per_page = 20

@admin.register(StatusAccount)
class StatusAccountAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']
    list_per_page = 20