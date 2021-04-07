#  ┏┳┓┏━┓╻┏┓╻
#  ┃┃┃┣━┫┃┃┗┫
#  ╹ ╹╹ ╹╹╹ ╹

terraform {
  required_providers {
    vsphere = {
      source  = "hashicorp/vsphere"
      version = "1.15.0"
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

locals {
  uploads = [
    for item in var.esxi_upload :
    {
      id        = sha256(join(" ", [item.datastore, item.destination]))
      datastore = item.datastore
      source    = item.source
      destination = format("/vmfs/volumes/%s/%s",
        item.datastore,
        can(regex("/$", item.destination)) ? basename(item.source) : trimprefix(item.destination, "/")
      )
      basename = can(regex("/$", item.destination)) ? basename(item.source) : basename(trimprefix(item.destination, "/"))
      dirname = format("/vmfs/volumes/%s/%s",
        item.datastore,
        trimprefix(dirname(item.destination), "/")
      )
      convert = item.vmdk_convert
    }
  ]
}

output "uploads" {
  value = yamlencode({ uploads = local.uploads })
}

resource "null_resource" "upload" {
  count = length(local.uploads)

  triggers = {
    source      = local.uploads[count.index].source
    datastore   = local.uploads[count.index].datastore
    destination = local.uploads[count.index].destination
    dirname     = local.uploads[count.index].destination
    basename    = local.uploads[count.index].destination
    convert     = local.uploads[count.index].convert
  }

  connection {
    type     = "ssh"
    host     = var.esxi_credentials.host
    port     = var.esxi_credentials.ssh_port
    user     = var.esxi_credentials.username
    password = var.esxi_credentials.password
  }

  provisioner "remote-exec" {
    inline = ["mkdir -p ${local.uploads[count.index].dirname}"]
  }

  provisioner "file" {
    source      = local.uploads[count.index].source
    destination = local.uploads[count.index].destination
  }

  provisioner "remote-exec" {
    inline = [
      local.uploads[count.index].convert ? <<-EOF
        set -ex
        cd '${local.uploads[count.index].dirname}'
        mv '${local.uploads[count.index].basename}' '${local.uploads[count.index].id}.vmdk'
        vmkfstools -d thin -i '${local.uploads[count.index].id}.vmdk' '${local.uploads[count.index].basename}'
        rm -f '${local.uploads[count.index].id}.vmdk'
      EOF
      : "true"
    ]
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
