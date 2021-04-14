#  ┏┳┓┏━┓╻┏┓╻
#  ┃┃┃┣━┫┃┃┗┫
#  ╹ ╹╹ ╹╹╹ ╹

terraform {
  required_providers {
    vsphere = {
      source  = "hashicorp/vsphere"
      version = "1.15.0"
    }
    macaddress = {
      source  = "ivoronin/macaddress"
      version = "0.2.2"
    }
  }
}

provider "vsphere" {
  user                 = var.esxi_credentials.username
  password             = var.esxi_credentials.password
  vsphere_server       = var.esxi_credentials.host
  allow_unverified_ssl = var.esxi_credentials.allow_unverified_ssl
}

locals {
  ssh_credentials = {
    username = var.esxi_credentials.username
    password = var.esxi_credentials.password
    host     = var.esxi_credentials.host
    port     = var.esxi_credentials.ssh_port
  }
  datastore       = "datastore1"
  ova_path        = "/ova/cdr-plugin-bd1ccee98b9b4cd1a10456f786c4405e6442bf85-21.ova"
  vmdk_path       = "/vmdk/${replace(basename(local.ova_path), ".ova", ".vmdk")}"
  vmdk_dhcpd_path = "/vmdk/dhcpd.vmdk"
}

#  ╻ ╻┏━┓╻  ┏━┓┏━┓╺┳┓
#  ┃ ┃┣━┛┃  ┃ ┃┣━┫ ┃┃
#  ┗━┛╹  ┗━╸┗━┛╹ ╹╺┻┛

module "upload_vm_vmdk" {
  source          = "./modules/upload"
  ssh_credentials = local.ssh_credentials

  src          = "../../ova/cdr-plugin-bd1ccee98b9b4cd1a10456f786c4405e6442bf85-21.ova"
  dest         = local.ova_path
  datastore    = local.datastore
  vmdk_convert = false
}

module "upload_dhcpd_vmdk" {
  source          = "./modules/upload"
  ssh_credentials = local.ssh_credentials

  src          = "../alpine-control-vmdk/alpine.vmdk"
  dest         = local.vmdk_dhcpd_path
  datastore    = local.datastore
  vmdk_convert = false
}

module "convert" {
  depends_on = [
    module.upload_vm_vmdk
  ]

  source          = "./modules/ova-to-vmdk"
  ssh_credentials = local.ssh_credentials

  datastore = local.datastore
  ova       = local.ova_path
  vmdk      = local.vmdk_path
}

#  ┏┓╻┏━╸╺┳╸╻ ╻┏━┓┏━┓╻┏ 
#  ┃┗┫┣╸  ┃ ┃╻┃┃ ┃┣┳┛┣┻┓
#  ╹ ╹┗━╸ ╹ ┗┻┛┗━┛╹┗╸╹ ╹

module "data" {
  source    = "./modules/data"
  datastore = local.datastore
}

module "network" {
  source        = "./modules/network"
  datacenter_id = module.data.datacenter_id
  host_id       = module.data.host_id
  nics          = ["vmnic1"]
}
#  ╺┳┓╻ ╻┏━╸┏━┓
#   ┃┃┣━┫┃  ┣━┛
#  ╺┻┛╹ ╹┗━╸╹  

module "dhcpd" {
  source = "./modules/vmdk"

  depends_on = [
    module.upload_dhcpd_vmdk
  ]

  ssh_credentials = local.ssh_credentials

  data = {
    pool_id        = module.data.pool_id
    datastore_id   = module.data.datastore_id
    datastore_name = module.data.datastore_name
    host_id        = module.data.host_id
    network_id     = module.network.id
  }

  instance_count = 1
  name_prefix    = "dhcpd"
  vmdk           = local.vmdk_dhcpd_path
  cpu            = 1
  ram            = 1024
}

#  ╻ ╻┏┳┓┏━┓
#  ┃┏┛┃┃┃┗━┓
#  ┗┛ ╹ ╹┗━┛

module "vms" {
  source = "./modules/vmdk"

  depends_on = [
    module.upload_vm_vmdk,
    module.dhcpd
  ]

  ssh_credentials = local.ssh_credentials

  data = {
    pool_id        = module.data.pool_id
    datastore_id   = module.data.datastore_id
    datastore_name = module.data.datastore_name
    host_id        = module.data.host_id
    network_id     = module.network.id
  }

  instance_count = 1
  name_prefix    = "demo"
  vmdk           = module.convert.path
  cpu            = 2
  ram            = 2048

  mac_addresses = slice(values(local.dhcp_address_mac), 0, 1)
}
