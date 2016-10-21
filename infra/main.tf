// Provider specific configs
provider "aws" {
    access_key = "${var.aws_access_key}"
    secret_key = "${var.aws_secret_key}"
    region = "${var.aws_region}"
}

# Our default security group to access
# the instances over SSH, HTTP, and HTTPS
resource "aws_security_group" "default" {
  name = "odp-web-${var.environment}"
  description = "SSH, HTTP, and HTTPS"

  # SSH access from anywhere
  ingress {
    from_port = 22
    to_port = 22
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # HTTP access from anywhere
  ingress {
    from_port = 80
    to_port = 80
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # HTTPS access from anywhere
  ingress {
    from_port = 443
    to_port = 443
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # outbound internet access
  egress {
    from_port = 0
    to_port = 0
    protocol = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

// EC2 Instance Resource for Module
resource "aws_instance" "app" {
    ami = "${var.ami_id}"
    instance_type = "${var.instance_type}"
    key_name = "${var.key_name}"
    security_groups = ["${aws_security_group.default.name}"]
    ebs_optimized = true
    root_block_device {
      volume_type = "gp2"
      volume_size = "${var.ebs_size}"
    }
    tags {
        created_by = "${lookup(var.tags,"created_by")}"
        Name = "${var.instance_name}-${var.environment}"
    }
}
