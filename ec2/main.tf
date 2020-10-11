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

output "ec2_result" {
  value = module.instance.public_dns
}
