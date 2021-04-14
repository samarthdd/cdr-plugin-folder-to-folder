#  ┏┳┓┏━┓╻┏┓╻
#  ┃┃┃┣━┫┃┃┗┫
#  ╹ ╹╹ ╹╹╹ ╹

terraform {
  required_providers {
    vsphere = {
      source  = "hashicorp/vsphere"
      version = "1.15.0"
    }
  }
}

resource "vsphere_host_virtual_switch" "this" {
  name           = var.switch_name
  host_system_id = var.host_id

  network_adapters = var.nics

  active_nics  = var.nics
  standby_nics = []
}

resource "vsphere_host_port_group" "this" {
  name                = var.port_group_name
  host_system_id      = var.host_id
  virtual_switch_name = vsphere_host_virtual_switch.this.name
}

data "vsphere_network" "this" {
  name          = vsphere_host_port_group.this.name
  datacenter_id = var.datacenter_id
}

