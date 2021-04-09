variable "esxi_upload" {
  type = list(object({
    source       = string
    datastore    = string
    destination  = string
    vmdk_convert = bool
  }))
  description = <<-EOF
List of files to upload via SSH. Object fields:
source - local path to the source file
datastore - name of the datastore on ESXi (example: datastore1)
destination - path to file in datastore (example: /my/folder/disk.vmdk; example: /; example: subf1/)
vmdk_convert - if true, will run vmkfstools in order to fix VMDK format
Note1: If destination ends with /, then source filename will be used
Note2: If destination includes filename at the end of the path, file will be saved under that name
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
    num_cpus  = number
    memory    = number
  }))
  description = "VirtualMachines to create"
  default     = []

  validation {
    condition = alltrue(concat(
      [for vm in var.vm : vm.num_cpus < 1 ? false : true],
      [for vm in var.vm : vm.memory < 1024 ? false : true],
    ))
    error_message = "Error: vm.num_cpus must be >= 1; vm.memory must be >= 1024."
  }
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
