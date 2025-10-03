# ============================================
# DOCKERFILE MULTI-STAGE - SendInvoice
# Python 3.12 + Django 5.2
# ============================================

# ========================================
# STAGE 1: Builder (Compilación)
# ========================================
FROM python:3.12-slim as builder

# Metadatos
LABEL maintainer="jcvargas1909@gmail.com"
LABEL description="SendInvoice - Builder Stage"
LABEL version="1.0"

# Variables de build
ARG DJANGO_ENV=production

# Información de por qué necesitamos cada paquete:
# gcc: Compilador C para paquetes que requieren compilación
# g++: Compilador C++ (algunos paquetes lo necesitan)
# libpq-dev: Headers de PostgreSQL para compilar psycopg2
# python3-dev: Headers de Python para compilar extensiones
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    libpq-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Directorio de trabajo
WORKDIR /app

# ============================================
# OPTIMIZACIÓN: Copiar solo requirements primero
# ============================================
# Esto aprovecha el sistema de cache de Docker
# Si solo cambias código (no requirements), esta capa se reutiliza
COPY requirements/base.txt requirements/prod.txt ./requirements/

# Instalar dependencias de Python
# --no-cache-dir: No guardar cache de pip (ahorra espacio)
# --upgrade pip: Usar última versión de pip
RUN python -m pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements/prod.txt

# ========================================
# STAGE 2: Runtime (Ejecución)
# ========================================
FROM python:3.12-slim

LABEL maintainer="jcvargas1909@gmail.com"
LABEL description="SendInvoice - Runtime Stage"

# ============================================
# VARIABLES DE ENTORNO CRÍTICAS
# ============================================

# PYTHONUNBUFFERED=1
# Propósito: Forzar que stdout y stderr no usen buffer
# Beneficio: Logs aparecen inmediatamente (crítico para debugging)
ENV PYTHONUNBUFFERED=1

# PYTHONDONTWRITEBYTECODE=1
# Propósito: No crear archivos .pyc (bytecode compilado)
# Beneficio: Imagen más liviana, menos I/O
ENV PYTHONDONTWRITEBYTECODE=1

# PIP_NO_CACHE_DIR=1
# Propósito: pip no guarda cache de descargas
# Beneficio: Imagen más pequeña
ENV PIP_NO_CACHE_DIR=1

# PIP_DISABLE_PIP_VERSION_CHECK=1
# Propósito: No verificar actualizaciones de pip
# Beneficio: Builds más rápidos
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# DJANGO_SETTINGS_MODULE
# Propósito: Define qué archivo de configuración usar
# Se sobrescribe con variables de entorno en docker-compose
ENV DJANGO_SETTINGS_MODULE=core.settings

# ============================================
# DEPENDENCIAS DE RUNTIME
# ============================================
# Solo instalamos librerías necesarias para EJECUTAR la app
# libpq5: Cliente de PostgreSQL (sin headers de compilación)
# postgresql-client: Cliente psql para el entrypoint
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# ============================================
# SEGURIDAD: Usuario no-root
# ============================================
# Principio de mínimo privilegio
# Si el contenedor es comprometido, el atacante NO tiene root
RUN groupadd -r django && useradd -r -g django -u 1000 django && \
    mkdir -p /app /app/staticfiles /app/media && \
    chown -R django:django /app

# Directorio de trabajo
WORKDIR /app

# ============================================
# COPIAR DEPENDENCIAS desde Builder
# ============================================
# Solo copiamos las librerías instaladas, no el código del builder
COPY --from=builder /usr/local/lib/python3.12/site-packages/ \
                    /usr/local/lib/python3.12/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# ============================================
# COPIAR CÓDIGO DE LA APLICACIÓN
# ============================================
# --chown=django:django: El usuario django es propietario
COPY --chown=django:django . .

# Cambiar al usuario no-root
USER django

# ============================================
# RECOLECTAR ARCHIVOS ESTÁTICOS
# ============================================
# Se ejecuta durante el BUILD, no en runtime
# --noinput: No preguntar confirmación
# --clear: Limpiar directorio antes de colectar
# Nota: collectstatic se ejecutará en el entrypoint, no aquí
# Razón: Necesita acceso a .env que se pasa en runtime

# ============================================
# EXPONER PUERTO
# ============================================
# Documenta que la app escucha en puerto 8000
# NO abre el puerto, solo es metadata
EXPOSE 8000

# ============================================
# HEALTHCHECK: Verificar que la app está viva
# ============================================
# Docker ejecuta este comando cada 30s
# Si falla 3 veces seguidas, marca el contenedor como unhealthy
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health/', timeout=2)" || exit 1

# ============================================
# ENTRYPOINT & CMD
# ============================================
# ENTRYPOINT: Script que corre migraciones y setup
ENTRYPOINT ["/entrypoint.sh"]

# CMD: Comando por defecto (se puede sobrescribir)
CMD ["gunicorn", \
     "core.wsgi:application", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "3", \
     "--worker-class", "sync", \
     "--timeout", "60", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "--log-level", "info"]