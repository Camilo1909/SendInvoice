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
from modules.auths.models import Account, StatusAccount, Role
try:
    state_active = StatusAccount.objects.get(id=1)
    print("✅ Estado 'Activo' ya existe.")
except StatusAccount.DoesNotExist:
    try:
        state_active = StatusAccount.objects.create(id=1, name="Activo")
        print("🟢 Estado 'Activo' creado.")
    except IntegrityError as e:
        print(f"⚠️ Error creando estado 'Activo': {e}")

try:
    state_inactive = StatusAccount.objects.get(id=2)
    print("✅ Estado 'Inactivo' ya existe.")
except StatusAccount.DoesNotExist:
    try:
        state_inactive = StatusAccount.objects.create(id=2, name="Inactivo")
        print("🟢 Estado 'Inactivo' creado.")
    except IntegrityError as e:
        print(f"⚠️ Error creando estado 'Inactivo': {e}")

# =========================
# ROLES (Role)
# =========================
try:
    role_owner = Role.objects.get(id=1)
    print("✅ Rol 'Owner' ya existe.")
except Role.DoesNotExist:
    try:
        role_owner = Role.objects.create(
            id=1,
            name="Owner",
            description="Rol dueño de la plataforma"
        )
        print("🟢 Rol 'Owner' creado.")
    except IntegrityError as e:
        print(f"⚠️ Error creando rol 'Owner': {e}")

try:
    role_admin = Role.objects.get(id=2)
    print("✅ Rol 'Admin' ya existe.")
except Role.DoesNotExist:
    try:
        role_admin = Role.objects.create(
            id=2,
            name="Admin",
            description="Rol administrador para cada compañía en la plataforma"
        )
        print("🟢 Rol 'Admin' creado.")
    except IntegrityError as e:
        print(f"⚠️ Error creando rol 'Admin': {e}")
try:
    if not Account.objects.filter(is_superuser=True).exists():
        print("Creando superusuario por defecto...")
        Account.objects.create_superuser(
            username='Admin',
            email='admin@sendinvoice.com',
            password='AdminDatabase@',
            role=role_owner,
            state=state_active
        )
        print("✅ Superusuario creado: admin/admin123")
    else:
        print("✅ Superusuario ya existe")
except Exception as e:
    print(f"⚠️ Error creando superusuario: {e}")
END

echo "======================================"
echo "✅ Inicialización completa!"
echo "======================================"

# Ejecutar el comando pasado como argumentos
exec "$@"