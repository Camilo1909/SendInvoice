output "db_instance_endpoint" {
  description = "Endpoint de conexión (host:puerto)"
  value       = aws_db_instance.postgres.endpoint
}

output "db_instance_address" {
  description = "DNS del RDS (sin puerto)"
  value       = aws_db_instance.postgres.address
}

output "db_instance_port" {
  description = "Puerto"
  value       = aws_db_instance.postgres.port
}

output "db_name" {
  description = "Nombre de la base de datos"
  value       = aws_db_instance.postgres.db_name
}

output "db_instance_id" {
  description = "ID de la instancia RDS"
  value       = aws_db_instance.postgres.id
}