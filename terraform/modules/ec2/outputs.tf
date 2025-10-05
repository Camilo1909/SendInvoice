output "instance_id" {
  description = "ID de la instancia EC2"
  value       = aws_instance.web.id
}

output "public_ip" {
  description = "IP pública del EC2"
  value       = aws_eip.web.public_ip
}

output "private_ip" {
  description = "IP privada del EC2"
  value       = aws_instance.web.private_ip
}

output "security_group_id" {
  description = "ID del Security Group"
  value       = aws_security_group.ec2.id
}