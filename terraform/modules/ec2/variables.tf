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

variable "public_subnet_ids" {
  description = "IDs de subnets públicas"
  type        = list(string)
}

variable "instance_type" {
  description = "Tipo de instancia EC2"
  type        = string
  default     = "t2.micro"
}

variable "ssh_key_name" {
  description = "Nombre de la llave SSH"
  type        = string
}

variable "my_ip" {
  description = "Tu IP pública para SSH"
  type        = string
}

variable "iam_instance_profile" {
  description = "IAM instance profile para el EC2"
  type        = string
  default     = ""
}