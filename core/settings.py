"""
Django settings for SendInvoice project.

MODIFICADO para soportar:
- Variables de entorno (.env)
- Docker
- Ambientes dev/prod
"""

from pathlib import Path

from decouple import Csv, config

# ============================================
# PATHS
# ============================================
BASE_DIR = Path(__file__).resolve().parent.parent

# ============================================
# SECURITY SETTINGS
# ============================================
SECRET_KEY = config(
    "SECRET_KEY", default="django-insecure-SOLO-PARA-DESARROLLO-CAMBIAR-EN-PRODUCCION"
)

# DEBUG
# Desarrollo: True | Producción: False
DEBUG = config("DEBUG", default=True, cast=bool)

# ALLOWED_HOSTS
# Desarrollo: ['localhost', '127.0.0.1']
# Producción: ['dominio.com']
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="localhost,127.0.0.1", cast=Csv())
CSRF_TRUSTED_ORIGINS = config(
    "CSRF_TRUSTED_ORIGINS", default=f"http://{ALLOWED_HOSTS[0]}", cast=Csv()
)

# ============================================
# APPLICATION DEFINITION
# ============================================
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
]

MODULES = [
    "modules.auths.apps.AuthsConfig",
    "modules.base.apps.BaseConfig",
    "modules.invoice.apps.InvoiceConfig",
    "modules.menu.apps.MenuConfig",
    "modules.services.apps.ServicesConfig",
]

INITIAL_APP = [
    "core",
]

AWS_APPS = [
    "storages",  # django-storages para AWS S3
]

INSTALLED_APPS += MODULES
INSTALLED_APPS += INITIAL_APP
INSTALLED_APPS += AWS_APPS

# =============================================
# MIDDLEWARE
# ============================================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # Whitenoise: Sirve archivos estáticos en producción
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

# ============================================
# TEMPLATES
# ============================================
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # context processor personalizado
                "modules.menu.context_processors.menu_items",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

# ============================================
# DATABASE
# ============================================

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DB_NAME", default="sendInvoice"),
        "USER": config("DB_USER", default="postgres"),
        "PASSWORD": config("DB_PASSWORD", default="postgres"),
        "HOST": config("DB_HOST", default="localhost"),
        "PORT": config("DB_PORT", default="5432"),
    }
}

# ============================================
# PASSWORD VALIDATION
# ============================================
# Modelo de usuario personalizado
AUTH_USER_MODEL = "auths.Account"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# ============================================
# INTERNATIONALIZATION
# ============================================
LANGUAGE_CODE = "es-co"
TIME_ZONE = "America/Bogota"
USE_I18N = True
USE_TZ = True

# ============================================
# STATIC FILES (CSS, JavaScript, Images)
# ============================================
STATIC_URL = "/static/"

# Directorios donde Django busca archivos estáticos
STATICFILES_DIRS = [BASE_DIR / "core" / "static"]

# Directorio donde collectstatic recolecta archivos (producción)
STATIC_ROOT = BASE_DIR / "staticfiles"

# ============================================
# MEDIA FILES (Archivos subidos por usuarios)
# ============================================
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

USE_S3 = config("USE_S3", default=False, cast=bool)

if USE_S3:
    # ========================================
    # AWS S3 Configuration
    # ========================================
    AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID", default=None)
    AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY", default=None)
    AWS_STORAGE_BUCKET_NAME_STATIC = config("AWS_STORAGE_BUCKET_NAME_STATIC")
    AWS_STORAGE_BUCKET_NAME_MEDIA = config("AWS_STORAGE_BUCKET_NAME_MEDIA")
    AWS_S3_REGION_NAME = config("AWS_S3_REGION_NAME", default="us-east-1")

    # AWS_ACCESS_KEY_ID: Usuario que puede escribir en S3
    # AWS_SECRET_ACCESS_KEY: Contraseña de ese usuario
    # AWS_STORAGE_BUCKET_NAME_STATIC: Nombre del bucket para CSS/JS
    # AWS_STORAGE_BUCKET_NAME_MEDIA: Nombre del bucket para facturas/logos
    # AWS_S3_REGION_NAME: Región donde están los buckets

    # ========================================
    # S3 Settings (optimización)
    # ========================================
    AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME_STATIC}.s3.amazonaws.com"
    # URL base: sendinvoice-static-prod.s3.amazonaws.com

    AWS_S3_OBJECT_PARAMETERS = {
        "CacheControl": "max-age=86400",  # Cache 24 horas
    }
    # Navegadores cachean archivos estáticos (más rápido)

    AWS_DEFAULT_ACL = None
    # None = No ACL por defecto (usa política del bucket)

    AWS_S3_FILE_OVERWRITE = False
    # False = No sobrescribir archivos con mismo nombre
    # Django agrega hash al nombre si ya existe

    # ========================================
    # Static Files en S3
    # ========================================
    STATICFILES_STORAGE = "core.storage_backends.StaticStorage"
    STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/static/"
    # URL final: https://sendinvoice-static-prod.s3.amazonaws.com/static/styles.css

    # ========================================
    # Media Files en S3
    # ========================================
    DEFAULT_FILE_STORAGE = "core.storage_backends.MediaStorage"
    MEDIA_URL = f"https://{AWS_STORAGE_BUCKET_NAME_MEDIA}.s3.amazonaws.com/media/"
    # URL final: https://sendinvoice-media-prod.s3.amazonaws.com/media/logo.png

else:
    # ========================================
    # Desarrollo Local (sin S3)
    # ========================================
    STATIC_URL = "/static/"
    STATIC_ROOT = BASE_DIR / "staticfiles"

    MEDIA_URL = "/media/"
    MEDIA_ROOT = BASE_DIR / "media"

# Whitenoise: Compresión y cache de archivos estáticos
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
        "OPTIONS": {
            "location": MEDIA_ROOT,
            "base_url": MEDIA_URL,
        },
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}


# ============================================
# DEFAULT PRIMARY KEY
# ============================================
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ============================================
# WHASTAPP API SETTINGS
# ============================================

WHATSAPP_API_TOKEN = config("WHATSAPP_API_TOKEN", default="")
WHATSAPP_PHONE_ID = config("WHATSAPP_PHONE_ID", default="")
WHATSAPP_API_URL = config(
    "WHATSAPP_API_URL", default="https://graph.facebook.com/v22.0/{WHATSAPP_PHONE_ID}/messages"
).format(WHATSAPP_PHONE_ID=WHATSAPP_PHONE_ID)

# ============================================
# CONFIGURACIÓN ESPECÍFICA DE PRODUCCIÓN
# ============================================
if not DEBUG:
    # Security settings para producción
    SECURE_PROXY_SSL_HEADER = (
        ("HTTP_X_FORWARDED_PROTO", "https") if config("SECURE_PROXY_SSL_HEADER") == "True" else None
    )
    SECURE_SSL_REDIRECT = config("SECURE_SSL_REDIRECT", default=True, cast=bool)
    SESSION_COOKIE_SECURE = config("SESESSION_COOKIE_SECURE", default=True, cast=bool)
    CSRF_COOKIE_SECURE = config("CSRF_COOKIE_SECURE", default=True, cast=bool)
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = "DENY"

    # HSTS (HTTP Strict Transport Security)
    SECURE_HSTS_SECONDS = 31536000  # 1 año
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
