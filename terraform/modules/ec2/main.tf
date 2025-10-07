# ============================================
# MÓDULO EC2 - SendInvoice
# Servidor con Docker para Django
# ============================================

# Security Group para EC2
resource "aws_security_group" "ec2" {
  name        = "${var.project_name}-ec2-sg-${var.environment}"
  description = "Security group para instancia EC2 con Django"
  vpc_id      = var.vpc_id

  # Inbound Rules (entrada)
  
  # HTTP (80) desde cualquier lugar
  ingress {
    description = "HTTP from anywhere"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # HTTPS (443) desde cualquier lugar
  ingress {
    description = "HTTPS from anywhere"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # SSH (22) solo desde TU IP
  ingress {
    description = "SSH from my IP"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.my_ip]
  }

  # Outbound Rules (salida) - permite TODO
  egress {
    description = "Allow all outbound"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"  # -1 = todos los protocolos
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.project_name}-ec2-sg-${var.environment}"
  }
}

# Obtener la AMI de Ubuntu más reciente
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"]  # Canonical (Ubuntu)

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

# Instancia EC2
resource "aws_instance" "web" {
  ami                    = data.aws_ami.ubuntu.id
  instance_type          = var.instance_type
  key_name               = var.ssh_key_name
  vpc_security_group_ids = [aws_security_group.ec2.id]
  subnet_id              = var.public_subnet_ids[0]  # Primera subnet pública

  # User data - script de inicialización
  user_data = templatefile("${path.module}/user_data.sh", {
    project_name = var.project_name
    environment  = var.environment
  })

  # Tamaño del disco (30GB Free Tier)
  root_block_device {
    volume_type           = "gp3"
    volume_size           = 30
    delete_on_termination = true
    encrypted             = true
  }

  # Metadata options (seguridad)
  metadata_options {
    http_endpoint               = "enabled"
    http_tokens                 = "required"  # IMDSv2 (más seguro)
    http_put_response_hop_limit = 1
  }

  tags = {
    Name = "${var.project_name}-web-${var.environment}"
  }
}

# Elastic IP (IP fija)
resource "aws_eip" "web" {
  instance = aws_instance.web.id
  domain   = "vpc"

  tags = {
    Name = "${var.project_name}-eip-${var.environment}"
  }
}