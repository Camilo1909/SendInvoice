"""
Django settings for SendInvoice project.

MODIFICADO para soportar:
- Variables de entorno (.env)
- Docker
- Ambientes dev/prod
"""

from pathlib import Path
from decouple import config, Csv

# ============================================
# PATHS
# ============================================
BASE_DIR = Path(__file__).resolve().parent.parent

# ============================================
# SECURITY SETTINGS
# ============================================
# ANTES: SECRET_KEY hardcodeado (INSEGURO)
# AHORA: Lee desde .env, con fallback para desarrollo
SECRET_KEY = config(
    'SECRET_KEY',
    default='django-insecure-SOLO-PARA-DESARROLLO-CAMBIAR-EN-PRODUCCION'
)

# DEBUG
# Desarrollo: True | Producción: False
DEBUG = config('DEBUG', default=True, cast=bool)

# ALLOWED_HOSTS
# Desarrollo: ['localhost', '127.0.0.1']
# Producción: ['tu-dominio.com']
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=Csv())

# ============================================
# APPLICATION DEFINITION
# ============================================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
]

# Tus módulos personalizados
MODULES = [
    "modules.auths.apps.AuthsConfig",
    "modules.base.apps.BaseConfig",
    "modules.invoice.apps.InvoiceConfig",
    "modules.menu.apps.MenuConfig"
]

INITIAL_APP = [
    "core",
]

INSTALLED_APPS += MODULES
INSTALLED_APPS += INITIAL_APP

# ============================================
# MIDDLEWARE
# ============================================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # Whitenoise: Sirve archivos estáticos en producción
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

# ============================================
# TEMPLATES
# ============================================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # Tu context processor personalizado
                'modules.menu.context_processors.menu_items',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# ============================================
# DATABASE
# ============================================
# ANTES: Credenciales hardcodeadas (INSEGURO)
# AHORA: Lee desde .env

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME', default='sendFacture'),
        'USER': config('DB_USER', default='postgres'),
        'PASSWORD': config('DB_PASSWORD', default='postgres'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}

# ============================================
# PASSWORD VALIDATION
# ============================================
# Modelo de usuario personalizado
AUTH_USER_MODEL = 'auths.Account'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# ============================================
# INTERNATIONALIZATION
# ============================================
LANGUAGE_CODE = 'es-co'
TIME_ZONE = 'America/Bogota'
USE_I18N = True
USE_TZ = True

# ============================================
# STATIC FILES (CSS, JavaScript, Images)
# ============================================
STATIC_URL = '/static/'

# Directorios donde Django busca archivos estáticos
STATICFILES_DIRS = [BASE_DIR / 'core' / 'static']

# Directorio donde collectstatic recolecta archivos (producción)
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Whitenoise: Compresión y cache de archivos estáticos
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# ============================================
# MEDIA FILES (Archivos subidos por usuarios)
# ============================================
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ============================================
# DEFAULT PRIMARY KEY
# ============================================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ============================================
# CONFIGURACIÓN ESPECÍFICA DE PRODUCCIÓN
# ============================================
if not DEBUG:
    # Security settings para producción
    SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=True, cast=bool)
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    
    # HSTS (HTTP Strict Transport Security)
    SECURE_HSTS_SECONDS = 31536000  # 1 año
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True