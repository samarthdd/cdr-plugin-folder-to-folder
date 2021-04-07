#  ┏┳┓┏━┓╻┏┓╻
#  ┃┃┃┣━┫┃┃┗┫
#  ╹ ╹╹ ╹╹╹ ╹

terraform {
  required_providers {
    vsphere = {
      source  = "hashicorp/vsphere"
      version = "1.25.0"
    }
    null = {
      source  = "hashicorp/null"
      version = "3.1.0"
    }
  }
}

provider "vsphere" {
  user                 = var.esxi_credentials.username
  password             = var.esxi_credentials.password
  vsphere_server       = var.esxi_credentials.host
  allow_unverified_ssl = var.esxi_credentials.allow_unverified_ssl
}

#  ╺┳┓┏━┓╺┳╸┏━┓
#   ┃┃┣━┫ ┃ ┣━┫
#  ╺┻┛╹ ╹ ╹ ╹ ╹

data "vsphere_datacenter" "this" {}

data "vsphere_resource_pool" "this" {}

data "vsphere_host" "host" {
  datacenter_id = data.vsphere_datacenter.this.id
}

#  ╻ ╻┏━┓╻  ┏━┓┏━┓╺┳┓
#  ┃ ┃┣━┛┃  ┃ ┃┣━┫ ┃┃
#  ┗━┛╹  ┗━╸┗━┛╹ ╹╺┻┛

resource "null_resource" "upload" {
  count = length(var.esxi_upload)

  triggers = {
    source      = var.esxi_upload[count.index].source
    datastore   = var.esxi_upload[count.index].datastore
    destination = var.esxi_upload[count.index].destination
  }

  connection {
    type     = "ssh"
    host     = var.esxi_credentials.host
    port     = var.esxi_credentials.ssh_port
    user     = var.esxi_credentials.username
    password = var.esxi_credentials.password
  }

  provisioner "file" {
    source = var.esxi_upload[count.index].source
    destination = format("/vmfs/volumes/%s/%s",
      var.esxi_upload[count.index].datastore,
      can(regex("/$", var.esxi_upload[count.index].destination)) ?
      basename(var.esxi_upload[count.index].source) :
      trimprefix(var.esxi_upload[count.index].destination, "/")
    )
  }
}

#  ╻ ╻┏┳┓┏━┓
#  ┃┏┛┃┃┃┗━┓
#  ┗┛ ╹ ╹┗━┛

data "vsphere_datastore" "vm" {
  count         = length(var.vm)
  name          = var.vm[count.index].datastore
  datacenter_id = data.vsphere_datacenter.this.id
}

data "vsphere_network" "vm" {
  count         = length(var.vm)
  name          = coalesce(var.vm[count.index].network, "VMs")
  datacenter_id = data.vsphere_datacenter.this.id
}

resource "vsphere_virtual_machine" "this" {
  count = length(var.vm)

  depends_on = [
    null_resource.upload
  ]

  name                       = var.vm[count.index].name
  resource_pool_id           = data.vsphere_resource_pool.this.id
  datastore_id               = data.vsphere_datastore.vm[count.index].id
  host_system_id             = data.vsphere_host.host.id
  wait_for_guest_net_timeout = 0
  wait_for_guest_ip_timeout  = 0
  guest_id                   = var.vm[count.index].guest_id

  disk {
    label        = "disk0"
    path         = var.vm[count.index].vmdk
    datastore_id = data.vsphere_datastore.vm[count.index].id
    attach       = true
  }

  network_interface {
    network_id = data.vsphere_network.vm[count.index].id
  }
}
