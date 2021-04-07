esxi_upload = [
  {
    source      = "./alpine/alpine.vmdk"
    datastore   = "datastore1"
    destination = "/"
  }
]

vm = [
  {
    name      = "test"
    vmdk      = "/alpine.vmdk"
    datastore = "datastore1"
    network   = "VMs"
    guest_id  = "ubuntu64Guest"
  }
]
