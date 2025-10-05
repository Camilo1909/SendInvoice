# ============================================
# VARIABLES DEL MÓDULO VPC
# ============================================

variable "vpc_cidr" {
  description = "CIDR block de la VPC"
  type        = string
}

variable "project_name" {
  description = "Nombre del proyecto"
  type        = string
}

variable "environment" {
  description = "Ambiente (dev, staging, prod)"
  type        = string
}