variable "esxi_upload" {
  type = list(object({
    source      = string
    datastore   = string
    destination = string
  }))
  description = <<-EOF
List of files to upload via SSH. Object fields:
source - local path to the source file
datastore - name of the datastore on ESXi (example: datastore1)
destination - path to file in datastore (example: /my/folder/disk.vmdk; example: /; example: subf1/)
Note1: If destination ends with /, then source filename will be used
Note2: destination must exists
Note3: If destination includes filename at the end of the path,  file will be saved under that name
EOF
  default     = []
}

variable "vm" {
  type = list(object({
    name      = string
    vmdk      = string
    datastore = string
    guest_id  = string
    network   = string
  }))
  description = "VirtualMachines to create"


}

variable "esxi_credentials" {
  type = object({
    username             = string
    password             = string
    host                 = string
    allow_unverified_ssl = bool
    ssh_port             = number
  })
  description = "ESXi connection details"
}
