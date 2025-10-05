variable "project_name" {
  description = "Nombre del proyecto"
  type        = string
}

variable "environment" {
  description = "Ambiente"
  type        = string
}

variable "vpc_id" {
  description = "ID de la VPC"
  type        = string
}

variable "private_subnet_ids" {
  description = "IDs de subnets privadas"
  type        = list(string)
}

variable "ec2_security_group_id" {
  description = "ID del Security Group del EC2"
  type        = string
}

variable "instance_class" {
  description = "Clase de instancia RDS"
  type        = string
  default     = "db.t3.micro"
}

variable "db_name" {
  description = "Nombre de la base de datos"
  type        = string
}

variable "db_username" {
  description = "Usuario maestro"
  type        = string
  sensitive   = true
}

variable "db_password" {
  description = "Contraseña de la BD"
  type        = string
  sensitive   = true
}