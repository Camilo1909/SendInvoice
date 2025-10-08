# ============================================
# MÓDULO IAM - SendInvoice
# Permisos para que EC2 acceda a S3
# ============================================

# ========================================
# IAM Role para EC2
# ========================================
resource "aws_iam_role" "ec2_s3_role" {
  name = "${var.project_name}-ec2-s3-role-${var.environment}"
  
  # Política de confianza (quién puede asumir este rol)
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })
  
  # Esta política dice:
  # "Las instancias EC2 pueden asumir este rol"
  
  tags = {
    Name = "${var.project_name}-ec2-s3-role-${var.environment}"
  }
}

# ========================================
# Política de permisos para S3
# ========================================
resource "aws_iam_policy" "s3_access" {
  name        = "${var.project_name}-s3-access-${var.environment}"
  description = "Permite acceso completo a buckets S3 de SendInvoice"
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "ListAllBuckets"
        Effect = "Allow"
        Action = "s3:ListAllMyBuckets"
        Resource = "*"
      },
      {
        Sid    = "ListBuckets"
        Effect = "Allow"
        Action = [
          "s3:ListBucket",
          "s3:GetBucketLocation"
        ]
        Resource = [
          var.static_bucket_arn,
          var.media_bucket_arn
        ]
      },
      {
        Sid    = "ObjectAccess"
        Effect = "Allow"
        Action = [
          "s3:PutObject",       # Subir archivos
          "s3:GetObject",       # Descargar archivos
          "s3:DeleteObject",    # Eliminar archivos
          "s3:PutObjectAcl"     # Cambiar permisos de archivos
        ]
        Resource = [
          "${var.static_bucket_arn}/*",
          "${var.media_bucket_arn}/*"
        ]
      }
    ]
  })
}

# Asociar política al rol
resource "aws_iam_role_policy_attachment" "ec2_s3_policy" {
  role       = aws_iam_role.ec2_s3_role.name
  policy_arn = aws_iam_policy.s3_access.arn
}

# ========================================
# Instance Profile (conecta rol con EC2)
# ========================================
resource "aws_iam_instance_profile" "ec2_profile" {
  name = "${var.project_name}-ec2-profile-${var.environment}"
  role = aws_iam_role.ec2_s3_role.name
  
  # ¿Qué es Instance Profile?
  # Es el "pegamento" entre el IAM Role y la instancia EC2
  # EC2 solo entiende "profiles", no "roles" directamente
}