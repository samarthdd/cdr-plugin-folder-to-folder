output "target_group_arn" {
    value = aws_lb_target_group.default.arn
}

output "alb_dns" {
  value = aws_lb.default.dns_name
}
