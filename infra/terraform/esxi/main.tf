# ESXI 01
module "sdk" {
  source         = "./ova"
  name_prefix    = "sdk"
  esxi_credentials = var.esxi_credentials1
  ovf_source     = var.ova_source.sdk
  instance_count = var.instance_counts1.sdk
  vcpu_count     = var.sdk_vcpu_count
  memory_mib     = var.sdk_memory_mib
  network        = var.network_esxi1
  datastore      = var.datastore_esxi1
}

module "offline_desktop" {
  source         = "./ova"
  name_prefix    = "offline-desktop"
  esxi_credentials = var.esxi_credentials1
  ovf_source     = var.ova_source.offline_desktop
  instance_count = var.instance_counts1.offline_desktop
  vcpu_count     = var.desktop_vcpu_count
  memory_mib     = var.desktop_memory_mib
  network        = var.network_esxi1
  datastore      = var.datastore_esxi1
}

module "workflow" {
  source         = "./ova"
  name_prefix    = "workflow"
  esxi_credentials = var.esxi_credentials1
  ovf_source     = var.ova_source.workflow
  instance_count = var.instance_counts1.workflow
  vcpu_count     = var.workflow_vcpu_count
  memory_mib     = var.workflow_memory_mib
  network        = var.network_esxi1
  datastore      = var.datastore_esxi1
}

# ESXI 02
module "sdk2" {
  source         = "./ova"
  name_prefix    = "sdk"
  esxi_credentials = var.esxi_credentials2
  ovf_source     = var.ova_source.sdk
  instance_count = var.instance_counts2.sdk
  vcpu_count     = var.sdk_vcpu_count
  memory_mib     = var.sdk_memory_mib
  network        = var.network_esxi2
  datastore      = var.datastore_esxi2
}

module "offline_desktop2" {
  source         = "./ova"
  name_prefix    = "offline-desktop"
  esxi_credentials = var.esxi_credentials2
  ovf_source     = var.ova_source.offline_desktop
  instance_count = var.instance_counts2.offline_desktop
  vcpu_count     = var.desktop_vcpu_count
  memory_mib     = var.desktop_memory_mib
  network        = var.network_esxi2
  datastore      = var.datastore_esxi2

}

module "workflow2" {
  source         = "./ova"
  name_prefix    = "workflow"
  esxi_credentials = var.esxi_credentials2
  ovf_source     = var.ova_source.workflow
  instance_count = var.instance_counts2.workflow
  vcpu_count     = var.workflow_vcpu_count
  memory_mib     = var.workflow_memory_mib
  network        = var.network_esxi2
  datastore      = var.datastore_esxi2
}

