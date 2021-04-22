module "esxi01" {
    source = "./esxi"
    esxi_credentials = var.esxi_credentials1
    instance_counts = var.instance_counts1
    ovf_urls = var.ova_urls
}

module "esxi02" {
    source = "./esxi"
    esxi_credentials = var.esxi_credentials2
    instance_counts = var.instance_counts2
    ova_urls = var.ova_urls
}

