module "vpc" {
  source = "./modules/vpc"

  vpc_cidr     = var.vpc_cidr
  project_name = var.project_name
  environment  = var.environment
}

module "ec2" {
  source = "./modules/ec2"

  project_name      = var.project_name
  environment       = var.environment
  vpc_id            = module.vpc.vpc_id
  public_subnet_ids = module.vpc.public_subnet_ids
  instance_type     = var.ec2_instance_type
  ssh_key_name      = var.ssh_key_name
  my_ip             = var.my_ip

  iam_instance_profile = module.iam.ec2_instance_profile_name
}

module "rds" {
  source = "./modules/rds"

  project_name          = var.project_name
  environment           = var.environment
  vpc_id                = module.vpc.vpc_id
  private_subnet_ids    = module.vpc.private_subnet_ids
  ec2_security_group_id = module.ec2.security_group_id
  instance_class        = var.rds_instance_class
  db_name               = var.db_name
  db_username           = var.db_username
  db_password           = var.db_password
}

module "s3" {
  source = "./modules/s3"

  project_name = var.project_name
  environment  = var.environment
  domain_name  = var.domain_name
}

# NUEVO: Módulo IAM
module "iam" {
  source = "./modules/iam"

  project_name      = var.project_name
  environment       = var.environment
  static_bucket_arn = module.s3.static_bucket_arn
  media_bucket_arn  = module.s3.media_bucket_arn
}