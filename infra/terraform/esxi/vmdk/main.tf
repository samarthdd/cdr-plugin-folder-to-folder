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

#  ╻ ╻┏┳┓╺┳┓╻┏ 
#  ┃┏┛┃┃┃ ┃┃┣┻┓
#  ┗┛ ╹ ╹╺┻┛╹ ╹

locals {
  vmdk_full_path = format("/vmfs/volumes/%s/%s",
    var.data.datastore_name,
    trimprefix(var.vmdk, "/")
  )
  workspace = [
    for index in range(var.instance_count) :
    {
      full_path      = format("%s/%s-%d", dirname(local.vmdk_full_path), var.name_prefix, index)
      datastore_path = format("%s/%s-%d", dirname(var.vmdk), var.name_prefix, index)
    }
  ]
  disks = [
    for index in range(var.instance_count) :
    {
      full_path      = "${local.workspace[index].full_path}/disk0.vmdk"
      datastore_path = "${local.workspace[index].datastore_path}/disk0.vmdk"
    }
  ]
}

resource "null_resource" "disk" {
  count = length(local.disks)

  triggers = {
    datastore   = var.data.datastore_name
    vmdk        = var.vmdk
    name_prefix = var.name_prefix
  }

  connection {
    type     = "ssh"
    host     = var.ssh_credentials.host
    port     = var.ssh_credentials.port
    user     = var.ssh_credentials.username
    password = var.ssh_credentials.password
  }

  provisioner "remote-exec" {
    inline = [
      <<-EOF
        set -ex
        SRC='${local.vmdk_full_path}'
        DEST='${local.disks[count.index].full_path}'
        mkdir -p "$(dirname "$DEST")"
        if [ ! -f "$DEST" ]; then
          vmkfstools -d thin -i "$SRC" "$DEST"
        fi
      EOF
    ]
  }
}

#  ╻ ╻┏┳┓┏━┓
#  ┃┏┛┃┃┃┗━┓
#  ┗┛ ╹ ╹┗━┛

resource "vsphere_virtual_machine" "this" {
  count = var.instance_count

  depends_on = [null_resource.disk]

  name                       = "${var.name_prefix}-${count.index}"
  resource_pool_id           = var.data.pool_id
  datastore_id               = var.data.datastore_id
  host_system_id             = var.data.host_id
  wait_for_guest_net_timeout = var.wait_for_guest_net_timeout
  wait_for_guest_ip_timeout  = var.wait_for_guest_ip_timeout
  guest_id                   = var.guest_id
  num_cpus                   = var.cpu
  memory                     = var.ram

  disk {
    label          = "disk0"
    datastore_id   = var.data.datastore_id
    path           = local.disks[count.index].datastore_path
    attach         = true
    keep_on_remove = false
  }

  network_interface {
    network_id = var.data.network_id
  }
}
