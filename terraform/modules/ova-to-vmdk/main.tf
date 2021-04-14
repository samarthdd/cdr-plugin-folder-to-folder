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
  ova_path = format("/vmfs/volumes/%s/%s",
    var.datastore,
    trimprefix(var.ova, "/")
  )
  vmdk_path = format("/vmfs/volumes/%s/%s",
    var.datastore,
    trimprefix(coalesce(var.vmdk, replace(var.ova, ".ova", ".vmdk")), "/")
  )
}

resource "null_resource" "converter" {
  triggers = {
    ova       = var.ova
    datastore = var.datastore
    ova_path  = local.ova_path
    vmdk_path = local.vmdk_path
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
        FOLDER='${dirname(local.vmdk_path)}'
        mkdir -p "$FOLDER" 
        cd "$FOLDER"
        VMDK_NAME="$(tar -tf '${local.ova_path}' | grep -iE '^.+\.vmdk$' | xargs tar -xpvf '${local.ova_path}')"
        mv "$VMDK_NAME" '${local.vmdk_path}'
      EOF
    ]
  }
}
