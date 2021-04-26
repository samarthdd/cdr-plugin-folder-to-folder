terraform {
  required_version = "~> 0.14"
  required_providers {
    esxi = {
      source  = "registry.terraform.io/josenk/esxi"
      version = "~> 1.8.1"
    }
    random = {
      source = "hashicorp/random"
      version = "3.1.0"
    }
  }
}

provider "esxi" {
  esxi_hostname = var.esxi_credentials.host
  esxi_hostport = var.esxi_credentials.ssh_port
  esxi_username = var.esxi_credentials.username
  esxi_password = var.esxi_credentials.password
}

resource "esxi_guest" "this" {
  count      = var.instance_count
  guest_name = "${var.name_prefix}-${var.random_string}-${count.index}"

  disk_store = var.datastore
  ovf_source = var.ovf_source

  numvcpus       = var.vcpu_count
  memsize        = var.memory_mib
  # boot_disk_size = var.boot_disk_size > 0 ? var.boot_disk_size : null

  power = var.auto_power_on ? "on" : "off"

  notes = "Instance #: ${count.index}|0ASource OVA/OVF URL: ${var.ovf_source}"

  network_interfaces {
    virtual_network = var.network
  }
}
