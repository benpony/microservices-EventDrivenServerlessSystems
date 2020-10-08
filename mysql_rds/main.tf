provider "aws" {
  region = "eu-west-3"
  profile = "default"
}

module "instance" {
  source                      = "git::https://github.com/cloudposse/terraform-aws-ec2-instance.git?ref=master"
  instance_type               = "t3.micro"
  vpc_id                      = "vpc-23203c4a"
  subnet                      = "subnet-0bc59770"
  name                        = "ec2demo"
  stage                       = "dev"
  ssh_key_pair                = ""
}

module "rds_instance" {
    source                      = "git::https://github.com/cloudposse/terraform-aws-rds.git?ref=master"
    namespace                   = "eg"
    name                        = "serverlessdemo"
    host_name                   = "db"
    ca_cert_identifier          = "rds-ca-2019"
    database_name               = "serverlessdemodb"
    database_user               = "admin"
    database_password           = "secretpassword"
    database_port               = 3306
    multi_az                    = true
    storage_type                = "gp2"
    allocated_storage           = 5
    storage_encrypted           = true
    engine                      = "mysql"
    engine_version              = "5.7.17"
    major_engine_version        = "5.7"
    instance_class              = "db.t3.micro"
    db_parameter_group          = "mysql5.7"
    publicly_accessible         = false
    subnet_ids                  = ["subnet-0bc59770","subnet-e7c8f38e","subnet-e7c8f38e"]
    vpc_id                      = "vpc-23203c4a"
}

output "ec2_result" {
  value = module.instance.public_dns
}

output "db_result" {
  value = module.rds_instance.hostname
}
