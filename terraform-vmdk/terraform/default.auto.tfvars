esxi_upload = [
  {
    source       = "./alpine/alpine.vmdk"
    datastore    = "datastore1"
    destination  = "/"
    vmdk_convert = true
  }
]

vm = [
  {
    name      = "test"
    vmdk      = "/alpine.vmdk"
    datastore = "datastore1"
    network   = "VMs"
    guest_id  = "ubuntu64Guest"
    num_cpus  = 4
    memory    = 4096
  }
]
