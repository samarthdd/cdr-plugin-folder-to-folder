module "esxi01" {
    source = "./esxi"
    esxi_credentials = var.esxi_credentials1
    instance_counts = var.instance_counts1
    ova_source = var.ova_source
}

module "esxi02" {
    source = "./esxi"
    esxi_credentials = var.esxi_credentials2
    instance_counts = var.instance_counts2
    ova_source = var.ova_source
}

