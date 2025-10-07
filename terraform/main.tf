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