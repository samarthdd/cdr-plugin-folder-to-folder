# Glasswall cloud SDK autoscaling group
module "gw_sdk_autoscaling" {
  source                    = "./modules/asg"
  project_name              = "${var.project}-${terraform.workspace}-sdk"
  vpc_id                    = var.vpc_id
  subnets                   = var.public_subnets
  image_id                  = var.sdk_image_id
  instance_type             = "t3.2xlarge"
  health_check_grace_period = 600
  desired_capacity          = var.sdk_desired_capacity
  min_instances             = var.sdk_min_instances
  max_instances             = var.sdk_max_instances
  user_data                 = false
  instance_port = {
    i-ssh     = ["ingress", "22", "TCP", [var.cidr_block]]
    i-https   = ["ingress", var.sdk_lb_port, "TCP", [var.cidr_block]]
    i-icap    = ["ingress", 1344, "TCP", [var.cidr_block]]
    e-default = ["egress", "0", "-1", ["0.0.0.0/0"]]
  }
  target_group_arns = [module.gw_sdk_loadbalancer.target_group_arn]
  tags              = var.common_tags
}

# Glasswall cloud SDK loadbalancer
module "gw_sdk_loadbalancer" {
  source            = "./modules/alb"
  project_name      = "${var.project}-${terraform.workspace}-sdk"
  target_port       = var.sdk_target_port
  lb_port           = [var.sdk_lb_port]
  health_check_path = "/api/health"
  instance_port     = var.sdk_lb_sgs
  subnets           = var.public_subnets
  vpc_id            = var.vpc_id
  tags              = var.common_tags
}

