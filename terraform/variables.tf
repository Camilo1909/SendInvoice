# ============================================
# VARIABLES GLOBALES - SendInvoice
# ============================================

# Región de AWS
variable "aws_region" {
  description = "Región de AWS donde se desplegará la infraestructura"
  type        = string
  default     = "us-east-1"

  # Validación: Solo regiones de US
  validation {
    condition     = can(regex("^us-", var.aws_region))
    error_message = "La región debe estar en US (us-east-1, us-west-2, etc.)"
  }
}

# Ambiente (dev, staging, prod)
variable "environment" {
  description = "Ambiente de despliegue"
  type        = string
  default     = "prod"

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Ambiente debe ser: dev, staging o prod"
  }
}

# Nombre del proyecto
variable "project_name" {
  description = "Nombre del proyecto"
  type        = string
  default     = "sendinvoice"
}

# CIDR de la VPC
variable "vpc_cidr" {
  description = "CIDR block para la VPC"
  type        = string
  default     = "10.0.0.0/16"

  # ¿Qué es CIDR? Rango de IPs
  # 10.0.0.0/16 = IPs desde 10.0.0.0 hasta 10.0.255.255
  # /16 = 65,536 IPs disponibles
}

# Tipo de instancia EC2
variable "ec2_instance_type" {
  description = "Tipo de instancia EC2"
  type        = string
  default     = "t2.micro" # ← Free Tier eligible
}

# Tipo de instancia RDS
variable "rds_instance_class" {
  description = "Clase de instancia RDS"
  type        = string
  default     = "db.t3.micro" # ← Free Tier eligible
}

# Base de datos
variable "db_name" {
  description = "Nombre de la base de datos"
  type        = string
  default     = "sendInvoice"
}

variable "db_username" {
  description = "Usuario maestro de la base de datos"
  type        = string
  default     = "postgres"
  sensitive   = true # ← No se muestra en logs
}

variable "db_password" {
  description = "Contraseña de la base de datos"
  type        = string
  sensitive   = true # ← CRÍTICO: No se muestra

  validation {
    condition     = length(var.db_password) >= 16
    error_message = "La contraseña debe tener al menos 16 caracteres"
  }
}

# Tu IP pública (para SSH)
variable "my_ip" {
  description = "Tu IP pública para acceso SSH"
  type        = string

  # Obtenla con: curl ifconfig.me
}

# SSH Key Name (la crearemos después)
variable "ssh_key_name" {
  description = "Nombre de la llave SSH en AWS"
  type        = string
  default     = "sendinvoice-key"
}