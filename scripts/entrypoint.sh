#!/bin/bash
# ============================================
# ENTRYPOINT para contenedor Django
# Se ejecuta cada vez que inicia el contenedor
# ============================================

set -e  # Detener si hay error

echo "======================================"
echo "🚀 Iniciando SendInvoice..."
echo "======================================"

# Esperar a que PostgreSQL esté listo
echo "⏳ Esperando PostgreSQL..."
while ! nc -z db 5432; do
  sleep 0.5
done
echo "✅ PostgreSQL listo!"

# Ejecutar migraciones
echo "🔄 Ejecutando migraciones..."
python manage.py migrate --noinput

# Recolectar archivos estáticos
echo "📦 Recolectando archivos estáticos..."
python manage.py collectstatic --noinput --clear

# Crear superusuario automáticamente (solo si no existe)
echo "👤 Verificando superusuario..."
python manage.py shell << END
from modules.auths.models import Account
if not Account.objects.filter(is_superuser=True).exists():
    print("Creando superusuario por defecto...")
    Account.objects.create_superuser(
        username='admin',
        email='admin@sendinvoice.com',
        password='admin123'
    )
    print("✅ Superusuario creado: admin/admin123")
else:
    print("✅ Superusuario ya existe")
END

echo "======================================"
echo "✅ Inicialización completa!"
echo "======================================"

# Ejecutar el comando pasado como argumentos
exec "$@"