ovf_urls = {
  sdk             = "https://glasswall-sow-ova.s3-eu-west-1.amazonaws.com/ova/centos-offline-csapi.ova"
  workflow        = "https://glasswall-sow-ova.s3-eu-west-1.amazonaws.com/vms/cdr-plugin/cdr-plugin-d501b83bbd8ae8456d2f1145b83b94eb7d69b90b-4.ova"
  offline_desktop = "https://glasswall-sow-ova.s3-eu-west-1.amazonaws.com/ova/OfflineDesktop.ova"
}

instances_count = {
  sdk             = 3
  workflow        = 3
  offline_desktop = 1
}
