# VPC Outputs
output "vpc_id" {
  description = "ID de la VPC"
  value       = module.vpc.vpc_id
}

# EC2 Outputs
output "ec2_public_ip" {
  description = "IP pública del EC2"
  value       = module.ec2.public_ip
}

output "ec2_instance_id" {
  description = "ID de la instancia EC2"
  value       = module.ec2.instance_id
}

# SSH Command
output "ssh_command" {
  description = "Comando para conectar por SSH"
  value       = "ssh -i ~/.ssh/sendinvoice-key.pem ubuntu@${module.ec2.public_ip}"
}

# RDS
output "rds_endpoint" {
  description = "Endpoint RDS (para .env)"
  value       = module.rds.db_instance_address
  sensitive   = true
}

output "rds_connection_string" {
  description = "String de conexión completo"
  value       = "postgresql://${var.db_username}:***@${module.rds.db_instance_address}:${module.rds.db_instance_port}/${var.db_name}"
  sensitive   = true
}