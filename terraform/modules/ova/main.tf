terraform {
  required_version = "~> 0.14"
  required_providers {
    esxi = {
      source  = "registry.terraform.io/josenk/esxi"
      version = "~> 1.8.1"
    }
  }
}

resource "esxi_guest" "this" {
  count      = var.instance_count
  guest_name = "${var.name_prefix}-${count.index}"

  disk_store = var.datastore
  ovf_source = var.ovf_source

  numvcpus       = var.vcpu_count
  memsize        = var.memory_mib
  boot_disk_size = var.boot_disk_size > 0 ? var.boot_disk_size : null

  power = var.auto_power_on ? "on" : "off"

  notes = <<-EOF
    Instance #: ${count.index}
    Source OVA/OVF URL: ${var.ovf_source}
  EOF

  guestinfo = var.guestinfo

  network_interfaces {
    virtual_network = var.network
  }
}
