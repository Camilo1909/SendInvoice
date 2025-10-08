# ============================================
# OUTPUTS del módulo S3
# Otros módulos usan estos valores
# ============================================

output "static_bucket_name" {
  description = "Nombre del bucket de static files"
  value       = aws_s3_bucket.static.id
}

output "static_bucket_arn" {
  description = "ARN del bucket static"
  value       = aws_s3_bucket.static.arn
}

output "static_bucket_domain" {
  description = "URL del bucket static"
  value       = aws_s3_bucket.static.bucket_regional_domain_name
  # Ejemplo: sendinvoice-static-prod.s3.us-east-1.amazonaws.com
}

output "media_bucket_name" {
  description = "Nombre del bucket de media files"
  value       = aws_s3_bucket.media.id
}

output "media_bucket_arn" {
  description = "ARN del bucket media"
  value       = aws_s3_bucket.media.arn
}

output "media_bucket_domain" {
  description = "URL del bucket media"
  value       = aws_s3_bucket.media.bucket_regional_domain_name
}