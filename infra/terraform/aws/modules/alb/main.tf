resource "aws_lb" "default" {
  name               = "${var.project_name}-lb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.default.id]
  subnets            = var.subnets

  enable_deletion_protection = false

  tags = var.tags
}

resource "aws_lb_target_group" "default" {
  name        = "${var.project_name}-tg"
  port        = var.target_port
  protocol    = var.target_protocol
  vpc_id      = var.vpc_id
  target_type = "instance"
  health_check {
    interval            = 60
    path                = var.health_check_path
    port                = var.target_port
    unhealthy_threshold = 2
    timeout             = 5
  }
}

resource "aws_lb_listener" "default" {
  count             = length(var.lb_port)
  load_balancer_arn = aws_lb.default.arn
  port              = var.lb_port[count.index]
  protocol          = var.lb_protocol[count.index]
  certificate_arn   = var.lb_protocol[count.index] == "HTTPS" ? var.certificate_arn : null

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.default.arn
  }
}

resource "aws_security_group" "default" {
  vpc_id      = var.vpc_id
  name        = "${var.project_name}-lb-sg"
  description = "Control the traffic to ALB"

  lifecycle {
    create_before_destroy = true
  }

  tags = merge(var.tags, map("Name", "${var.project_name}-sg"))
}

resource "aws_security_group_rule" "rule" {
  count             = length(var.instance_port)
  protocol          = element(var.instance_port[element(keys(var.instance_port), count.index)], 2)
  from_port         = element(var.instance_port[element(keys(var.instance_port), count.index)], 1)
  to_port           = element(var.instance_port[element(keys(var.instance_port), count.index)], 1)
  type              = element(var.instance_port[element(keys(var.instance_port), count.index)], 0)
  cidr_blocks       = element(var.instance_port[element(keys(var.instance_port), count.index)], 3)
  security_group_id = aws_security_group.default.id
}

