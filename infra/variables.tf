// Module specific variables
// https://github.com/bitzesty/qae-terraform
// https://github.com/terraform-community-modules/tf_aws_ec2_instance
// https://github.com/hashicorp/terraform/pull/5236
// https://cloud-images.ubuntu.com/locator/ec2/

variable "instance_name" {
  description = "Used to populate the Name tag. This is done in main.tf"
}

variable "environment" {
  description = "Environment name (staging, production)"
}

variable "instance_type" {}

variable "ami_id" {
  description = "The AMI to use"
}

variable "key_name" {
  description = "Name of EC2 key pair"
}

variable "availability_zone" {
  description = "EBS availability zone"
  default = "us-east-1b"
}

variable "ebs_size" {
  description = "EBS volume size in GB"
}

variable "tags" {
  default = {
    created_by = "terraform"
 }
}

// Variables for providers used in this module
variable "aws_access_key" {}
variable "aws_secret_key" {}
variable "aws_region" {}
