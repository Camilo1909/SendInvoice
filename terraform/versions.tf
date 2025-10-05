# ============================================
# VERSIONES Y PROVIDERS
# ============================================

# Versión mínima de Terraform
terraform {
  required_version = ">= 1.6.0"

  # Providers requeridos
  required_providers {
    aws = {
      source  = "hashicorp/aws" # ← Proveedor oficial de AWS
      version = "~> 5.0"        # ← Versión 5.x (última estable)
    }
  }

  # Backend para guardar el estado (por ahora local)
  # Después lo cambiaremos a S3
  backend "local" {
    path = "terraform.tfstate"
  }
}

# Configuración del provider AWS
provider "aws" {
  region = var.aws_region # ← Lee de variables.tf

  # Tags por defecto para TODOS los recursos
  default_tags {
    tags = {
      Project     = "SendInvoice"
      ManagedBy   = "Terraform"
      Environment = var.environment
      Owner       = "DevOps-Juan Camilo"
    }
  }
}