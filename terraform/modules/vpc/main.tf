# ============================================
# MÓDULO VPC - SendInvoice
# Crea la red virtual en AWS
# ============================================

# Crear la VPC
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true # ← Permite DNS interno (importante para RDS)
  enable_dns_support   = true

  tags = {
    Name = "${var.project_name}-vpc-${var.environment}"
  }
}

# Internet Gateway (puerta de salida a Internet)
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "${var.project_name}-igw-${var.environment}"
  }
}

# Subnet Pública (para EC2)
resource "aws_subnet" "public" {
  count = 2 # ← Creamos 2 subnets (high availability)

  vpc_id                  = aws_vpc.main.id
  cidr_block              = cidrsubnet(var.vpc_cidr, 8, count.index)
  availability_zone       = data.aws_availability_zones.available.names[count.index]
  map_public_ip_on_launch = true # ← Auto-asignar IP pública

  tags = {
    Name = "${var.project_name}-public-subnet-${count.index + 1}-${var.environment}"
    Type = "public"
  }
}

# Subnet Privada (para RDS)
resource "aws_subnet" "private" {
  count = 2

  vpc_id            = aws_vpc.main.id
  cidr_block        = cidrsubnet(var.vpc_cidr, 8, count.index + 2)
  availability_zone = data.aws_availability_zones.available.names[count.index]

  tags = {
    Name = "${var.project_name}-private-subnet-${count.index + 1}-${var.environment}"
    Type = "private"
  }
}

# Route Table para Subnets Públicas
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  # Ruta a Internet
  route {
    cidr_block = "0.0.0.0/0"                  # ← Todo el tráfico
    gateway_id = aws_internet_gateway.main.id # ← Sale por IGW
  }

  tags = {
    Name = "${var.project_name}-public-rt-${var.environment}"
  }
}

# Asociar Route Table con Subnets Públicas
resource "aws_route_table_association" "public" {
  count = 2

  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}

# Data source: Obtener Availability Zones disponibles
data "aws_availability_zones" "available" {
  state = "available"
}
