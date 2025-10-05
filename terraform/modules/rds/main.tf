# ============================================
# MÓDULO RDS - PostgreSQL para SendInvoice
# ============================================

# DB Subnet Group (define dónde puede correr RDS)
resource "aws_db_subnet_group" "main" {
  name       = "${var.project_name}-db-subnet-group-${var.environment}"
  subnet_ids = var.private_subnet_ids

  tags = {
    Name = "${var.project_name}-db-subnet-group-${var.environment}"
  }
}

# Security Group para RDS
resource "aws_security_group" "rds" {
  name        = "${var.project_name}-rds-sg-${var.environment}"
  description = "Security group para RDS PostgreSQL"
  vpc_id      = var.vpc_id

  ingress {
    description     = "PostgreSQL from EC2"
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [var.ec2_security_group_id]
  }

  egress {
    description = "Allow all outbound"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.project_name}-rds-sg-${var.environment}"
  }
}

# Parameter Group
resource "aws_db_parameter_group" "postgres" {
  name   = "${var.project_name}-postgres17-${var.environment}"
  family = "postgres17"

  parameter {
    name  = "max_connections"
    value = "100"
    apply_method = "pending-reboot"
  }

  tags = {
    Name = "${var.project_name}-postgres17-params-${var.environment}"
  }
}

# RDS Instance
resource "aws_db_instance" "postgres" {
  identifier = "${var.project_name}-db-${var.environment}"

  # Motor
  engine               = "postgres"
  engine_version       = "17.6"
  instance_class       = var.instance_class
  
  # Almacenamiento (Free Tier: 20GB)
  allocated_storage     = 20
  max_allocated_storage = 20  # No auto-scaling (evita costos)
  storage_type          = "gp3"
  storage_encrypted     = true

  # Credenciales
  db_name  = var.db_name
  username = var.db_username
  password = var.db_password
  port     = 5432

  # Red
  db_subnet_group_name   = aws_db_subnet_group.main.name
  vpc_security_group_ids = [aws_security_group.rds.id]
  publicly_accessible    = false

  # Backups (Free Tier: 7 días)
  backup_retention_period = 7
  backup_window          = "03:00-04:00"  # 3am UTC
  maintenance_window     = "sun:04:00-sun:05:00"

  # Configuración
  parameter_group_name = aws_db_parameter_group.postgres.name
  
  # Performance Insights (opcional, 7 días gratis)
  # enabled_cloudwatch_logs_exports = ["postgresql", "upgrade"]
  
  # Multi-AZ (false para Free Tier)
  multi_az = false

  # Protección
  deletion_protection       = true  # Evita borrado accidental
  skip_final_snapshot      = false
  final_snapshot_identifier = "${var.project_name}-final-snapshot-${var.environment}"
  
  # Auto minor version upgrades
  auto_minor_version_upgrade = true

  tags = {
    Name = "${var.project_name}-db-${var.environment}"
  }
}