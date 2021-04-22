variable "project_name" {
  type = string
  default = "aws-asg"
}

variable "min_instances" {
  type = number
  default = 1
}

variable "max_instances" {
  type = number
  default = 1
}

variable "desired_capacity" {
  type = number
  description = "Desired number of instances in the autoscaling group"
}

variable "instance_type" {
  type = string
  default = "t2.medium"
}

variable "image_id" {
  type = string
  default = "ami-0425ca41d2dc3a432"
}

variable "key_name" {
  type = string
  default = "packer"
}

variable "instance_port" {
  default = {
    i-ssh     = ["ingress", "22", "TCP", ["0.0.0.0/0"]]
    i-https     = ["ingress", "443", "TCP", ["0.0.0.0/0"]]
    e-default = ["egress", "0", "-1", ["0.0.0.0/0"]]
  }
}

variable "subnets" {
  type = list
}

variable "vpc_id" {
  type = string
}

variable "tags" {
  type = map(string)
}

variable "health_check_grace_period" {
  type = number
  description = "Health check grace period in seconds"
}

variable "target_group_arns" {
  type = list
}

variable "gw_sdk_address" {
  type = string
  default = ""
}

variable "user_data" {
  default = false
}

variable "args" {
  type = string
  default = ""
  description = "args for cloud init script"
}
