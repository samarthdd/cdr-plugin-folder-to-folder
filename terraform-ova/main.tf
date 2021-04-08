terraform {
  required_version = "~> 0.14"
  required_providers {
    esxi = {
      source  = "registry.terraform.io/josenk/esxi"
      version = "~> 1.8.1"
    }
  }
}

provider "esxi" {
  esxi_hostname = var.esxi_credentials.host
  esxi_hostport = var.esxi_credentials.ssh_port
  esxi_hostssl  = var.esxi_credentials.ssl_port
  esxi_username = var.esxi_credentials.username
  esxi_password = var.esxi_credentials.password
}

resource "esxi_guest" "this" {
  count      = var.instance_count
  guest_name = "${var.name_prefix}-${count.index}"

  disk_store = var.datastore
  ovf_source = var.ovf_source

  network_interfaces {
    virtual_network = var.network
  }
}
