provider "aws" {
  region = "eu-west-3"
  profile = "default"
}

module "instance" {
  source                      = "git::https://github.com/cloudposse/terraform-aws-ec2-instance.git?ref=master"
  instance_type               = "t3.micro"
  vpc_id                      = "vpc-23203c4a"
  subnet                      = "subnet-0bc59770"
  name                        = "ec2serverlessdemodemo"
  stage                       = "dev"
  ssh_key_pair                = ""
}

resource "aws_security_group_rule" "allow-all" {
  type              = "ingress"
  from_port         = 3306
  to_port           = 3306
  protocol          = "tcp"
  cidr_blocks = ["0.0.0.0/0"]
  security_group_id = "sg-0ede510e68e6d6578"
}

module "rds_instance" {
    source                      = "git::https://github.com/cloudposse/terraform-aws-rds.git?ref=master"
    name                        = "serverlessdemo"
    host_name                   = "db"
    ca_cert_identifier          = "rds-ca-2019"
    database_name               = "serverlessdemodb"
    database_user               = "admin"
    database_password           = "secretpassword"
    database_port               = 3306
    multi_az                    = true
    storage_type                = ""
    allocated_storage           = 5
    storage_encrypted           = true
    engine                      = "mysql"
    engine_version              = "8.0.20"
    instance_class              = "db.t3.micro"
    db_parameter_group          = "mysql8.0"
    publicly_accessible         = true
    subnet_ids                  = ["subnet-0bc59770","subnet-e7c8f38e","subnet-e7c8f38e"]
    vpc_id                      = "vpc-23203c4a"
    security_group_ids = ["sg-0ede510e68e6d6578"]
}

output "ec2_result" {
  value = module.instance.public_dns
}

output "db_result" {
  value = module.rds_instance.instance_address
}
