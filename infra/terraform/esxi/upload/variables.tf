variable "src" {
  type        = string
  description = "Path to local file"
}

variable "datastore" {
  type        = string
  description = "Name of datastore to use"
  default     = "datastore1"
}

variable "dest" {
  type        = string
  description = "Path to save file in datastore"
  default     = "/"
}

variable "vmdk_convert" {
  type        = bool
  description = "If true, postprocess the VMDK file using vmkfstools"
  default     = false
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
