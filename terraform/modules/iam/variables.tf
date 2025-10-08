variable "project_name" {
  description = "Nombre del proyecto"
  type        = string
}

variable "environment" {
  description = "Ambiente"
  type        = string
}

variable "static_bucket_arn" {
  description = "ARN del bucket de static files"
  type        = string
}

variable "media_bucket_arn" {
  description = "ARN del bucket de media files"
  type        = string
}