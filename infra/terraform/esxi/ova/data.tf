data "template_file" "default" {
  count = length(var.ip_addresses)
  template = file("${path.module}/${var.name_prefix}_init.tpl")
  vars = {
    "ip_address" = var.ip_addresses[count.index]
    "gateway_ip" = var.gateway_ips[count.index]
  }
}
