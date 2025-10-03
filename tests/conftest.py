"""
Configuración global de pytest para SendInvoice
"""

import os

import django
from django.conf import settings

# Setup Django antes de importar modelos
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")


def pytest_configure(config):
    """
    Configuración personalizada de pytest
    """
    # Forzar configuración de test ANTES de django.setup()
    from django.conf import settings as django_settings

    # Configurar BD para tests con TODOS los parámetros necesarios
    django_settings.DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": ":memory:",
            "ATOMIC_REQUESTS": False,
            "AUTOCOMMIT": True,
            "CONN_MAX_AGE": 0,
            "OPTIONS": {},
            "TIME_ZONE": None,
            "USER": "",
            "PASSWORD": "",
            "HOST": "",
            "PORT": "",
        }
    }

    # Deshabilitar migraciones complejas para tests (más rápido)
    # django_settings.MIGRATION_MODULES = {
    #     app: None for app in django_settings.INSTALLED_APPS
    # }


# Setup Django después de configurar
django.setup()
