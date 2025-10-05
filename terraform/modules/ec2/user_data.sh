#!/bin/bash
# ============================================
# USER DATA SCRIPT - SendInvoice EC2
# Se ejecuta la primera vez que arranca el EC2
# ============================================

set -e  # Detener si hay error

# Logging
exec > >(tee /var/log/user-data.log)
exec 2>&1

echo "================================================"
echo "Iniciando configuración de EC2 - ${project_name}"
echo "Ambiente: ${environment}"
echo "Fecha: $(date)"
echo "================================================"

# Actualizar sistema
echo ">>> Actualizando sistema..."
apt-get update -y
apt-get upgrade -y

# Instalar dependencias
echo ">>> Instalando dependencias..."
apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release \
    git \
    make \
    unzip \
    htop \
    vim

# Instalar Docker
echo ">>> Instalando Docker..."
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
usermod -aG docker ubuntu  # Agregar usuario ubuntu al grupo docker

# Instalar Docker Compose
echo ">>> Instalando Docker Compose..."
DOCKER_COMPOSE_VERSION="2.24.0"
curl -L "https://github.com/docker/compose/releases/download/v$${DOCKER_COMPOSE_VERSION}/docker-compose-$(uname -s)-$(uname -m)" \
    -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Verificar instalaciones
echo ">>> Verificando instalaciones..."
docker --version
docker-compose --version

# Crear directorio para la aplicación
echo ">>> Creando directorio de aplicación..."
mkdir -p /opt/${project_name}
chown ubuntu:ubuntu /opt/${project_name}

# Configurar Docker para iniciar automáticamente
echo ">>> Configurando Docker para auto-inicio..."
systemctl enable docker
systemctl start docker

# Configurar swap (mejora performance con 1GB RAM)
echo ">>> Configurando swap..."
fallocate -l 2G /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
echo '/swapfile none swap sw 0 0' >> /etc/fstab

# Configurar límites del sistema
echo ">>> Configurando límites del sistema..."
cat >> /etc/sysctl.conf << EOF
# Configuración para Django + PostgreSQL
vm.swappiness=10
vm.overcommit_memory=1
net.core.somaxconn=65535
EOF
sysctl -p

# Instalar AWS CLI v2
echo ">>> Instalando AWS CLI..."
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
./aws/install
rm -rf aws awscliv2.zip

# Configurar cloudwatch agent (para logs)
echo ">>> Configurando CloudWatch Agent..."
wget https://s3.amazonaws.com/amazoncloudwatch-agent/ubuntu/amd64/latest/amazon-cloudwatch-agent.deb
dpkg -i amazon-cloudwatch-agent.deb
rm amazon-cloudwatch-agent.deb

# Crear script de deployment
echo ">>> Creando script de deployment..."
cat > /opt/${project_name}/deploy.sh << 'DEPLOY_SCRIPT'
#!/bin/bash
set -e

echo "Iniciando deployment..."

# Ir al directorio de la app
cd /opt/${project_name}

# Pull de la imagen más reciente
docker-compose pull

# Detener contenedores
docker-compose down

# Iniciar con la nueva imagen
docker-compose up -d

# Ver logs
docker-compose logs -f
DEPLOY_SCRIPT

chmod +x /opt/${project_name}/deploy.sh
chown ubuntu:ubuntu /opt/${project_name}/deploy.sh

# Configurar firewall (ufw)
echo ">>> Configurando firewall..."
ufw --force enable
ufw default deny incoming
ufw default allow outgoing
ufw allow 22/tcp   # SSH
ufw allow 80/tcp   # HTTP
ufw allow 443/tcp  # HTTPS
ufw allow 8000/tcp # Django dev (temporal)

echo "================================================"
echo "Configuración completada exitosamente"
echo "Fecha: $(date)"
echo "================================================"

# Reiniciar para aplicar todos los cambios
echo ">>> Reiniciando sistema..."
reboot