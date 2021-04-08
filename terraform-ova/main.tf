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

module "sdk" {
  source         = "./esxi-instance"
  name_prefix    = "sdk"
  ovf_source     = var.ovf_urls.sdk
  instance_count = 2
  vcpu_count     = 4
  memory_mib     = 2048
}

module "offline_desktop" {
  source         = "./esxi-instance"
  name_prefix    = "offline-desktop"
  ovf_source     = var.ovf_urls.offline_desktop
  instance_count = 1
  vcpu_count     = 2
  memory_mib     = 2048
}

module "workflow" {
  source         = "./esxi-instance"
  name_prefix    = "workflow"
  ovf_source     = var.ovf_urls.workflow
  instance_count = 1
  vcpu_count     = 2
  memory_mib     = 2048
}
