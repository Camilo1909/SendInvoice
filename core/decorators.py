# auths/decorators.py
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from modules.auths.models import Account

def role_required(*role_names):
    """
    Decorador que verifica si el usuario tiene alguno de los roles especificados
    Uso: @role_required('Owner', 'Admin')
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapper(request, *args, **kwargs):
            account = Account.getAccount(request.user)
            
            if not account:
                messages.error(request, "No tienes una cuenta válida.")
                return redirect('login')
            
            # Verificar si tiene alguno de los roles requeridos
            user_roles = account.rol.values_list('name', flat=True)
            has_required_role = any(role in user_roles for role in role_names)
            
            if not has_required_role:
                messages.error(
                    request, 
                    f"No tienes permiso para acceder a esta sección. Se requiere uno de los siguientes roles: {', '.join(role_names)}"
                )
                raise PermissionDenied
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

def owner_required(view_func):
    """
    Decorador específico para Owner
    Uso: @owner_required
    """
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        account = Account.getAccount(request.user)
        
        if not account:
            messages.error(request, "No tienes una cuenta válida.")
            return redirect('login')
        
        # Verificar si tiene el rol Owner
        has_owner_role = account.rol.filter(name__iexact='Owner').exists()
        
        if not has_owner_role:
            messages.error(request, "Solo los Owners pueden acceder a esta sección.")
            raise PermissionDenied
        
        return view_func(request, *args, **kwargs)
    return wrapper

def company_required(view_func):
    """
    Decorador que verifica que el usuario tenga compañía asignada
    Uso: @company_required
    """
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        account = Account.getAccount(request.user)
        
        if not account:
            messages.error(request, "No tienes una cuenta válida.")
            return redirect('login')
        
        # Los Owners y superusuarios pueden acceder a todo
        is_owner = account.rol.filter(name__iexact='Owner').exists()
        if is_owner or account.is_superuser:
            return view_func(request, *args, **kwargs)
        
        # Otros usuarios deben tener compañía
        if not account.company:
            messages.error(request, "No tienes una compañía asignada.")
            raise PermissionDenied
        
        return view_func(request, *args, **kwargs)
    return wrapper

def owner_or_role_required(*role_names):
    """
    Decorador que permite acceso a Owners o usuarios con roles específicos
    Uso: @owner_or_role_required('Admin', 'Manager')
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapper(request, *args, **kwargs):
            account = Account.getAccount(request.user)
            
            if not account:
                messages.error(request, "No tienes una cuenta válida.")
                return redirect('login')
            
            # Verificar si es Owner o superusuario
            is_owner = account.rol.filter(name__iexact='Owner').exists()
            if is_owner or account.is_superuser:
                return view_func(request, *args, **kwargs)
            
            # Verificar roles específicos
            user_roles = account.rol.values_list('name', flat=True)
            has_required_role = any(role in user_roles for role in role_names)
            
            if not has_required_role:
                messages.error(
                    request, 
                    f"No tienes permiso para acceder a esta sección. Se requiere uno de los siguientes roles: {', '.join(role_names)}"
                )
                raise PermissionDenied
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

def superuser_required(view_func):
    """
    Decorador específico para superusuarios
    Uso: @superuser_required
    """
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if not request.user.is_superuser:
            messages.error(request, "Solo los superusuarios pueden acceder a esta sección.")
            raise PermissionDenied
        
        return view_func(request, *args, **kwargs)
    return wrapper