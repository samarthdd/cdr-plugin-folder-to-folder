variable "ova" {
  type        = string
  description = "Path to OVA in the datastore"
}

variable "datastore" {
  type        = string
  description = "Name of datastore to use"
  default     = "datastore1"
}

variable "vmdk" {
  type        = string
  description = "Path to result .vmdk (optional)"
  default     = null
}

variable "ssh_credentials" {
  type = object({
    username = string
    password = string
    host     = string
    port     = number
  })
  description = "ESXi SSH connection details"
}
