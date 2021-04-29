data "template_file" "default" {
  template = file("${path.module}/${var.name_prefix}_init.tpl")
  vars = {
    "ip_address" = var.ip_address
    "gateway_ip" = var.gateway_ip
  }
}
