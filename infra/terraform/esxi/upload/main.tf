#  ┏┳┓┏━┓╻┏┓╻
#  ┃┃┃┣━┫┃┃┗┫
#  ╹ ╹╹ ╹╹╹ ╹

terraform {
  required_providers {
    null = {
      source  = "hashicorp/null"
      version = "3.1.0"
    }
  }
}

#  ╻ ╻┏━┓╻  ┏━┓┏━┓╺┳┓
#  ┃ ┃┣━┛┃  ┃ ┃┣━┫ ┃┃
#  ┗━┛╹  ┗━╸┗━┛╹ ╹╺┻┛

locals {
  id = sha256(join(" ", [var.datastore, var.dest]))
  path = format("/vmfs/volumes/%s/%s",
    var.datastore,
    can(regex("/$", var.dest)) ? basename(var.src) : trimprefix(var.dest, "/")
  )
  basename = can(regex("/$", var.dest)) ? basename(var.src) : basename(trimprefix(var.dest, "/"))
  dirname = format("/vmfs/volumes/%s/%s",
    var.datastore,
    trimprefix(dirname(var.dest), "/")
  )
}

resource "null_resource" "upload" {
  triggers = {
    source    = var.src
    datastore = var.datastore
    path      = local.path
    dirname   = local.dirname
    basename  = local.basename
    convert   = var.vmdk_convert
  }

  connection {
    type     = "ssh"
    host     = var.ssh_credentials.host
    port     = var.ssh_credentials.port
    user     = var.ssh_credentials.username
    password = var.ssh_credentials.password
  }

  provisioner "remote-exec" {
    inline = ["mkdir -p ${local.dirname}"]
  }

  provisioner "file" {
    source      = var.src
    destination = local.path
  }

  provisioner "remote-exec" {
    inline = [
      var.vmdk_convert ? <<-EOF
        set -ex
        cd '${local.dirname}'
        mv '${local.basename}' '${local.id}.vmdk'
        vmkfstools -d thin -i '${local.id}.vmdk' '${local.basename}'
        rm -f '${local.id}.vmdk'
      EOF
      : "true"
    ]
  }
}
