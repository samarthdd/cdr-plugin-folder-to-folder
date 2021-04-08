variable "esxi_credentials" {
  type = object({
    username = string
    password = string
    host     = string
    ssh_port = number
    ssl_port = number
  })
  description = "ESXi connection details"
}

variable "instance_count" {
  type        = number
  description = "Count of instances"
  default     = 1
}

variable "name_prefix" {
  type        = string
  description = "Name prefix for the instances"
  default     = "sdk"
}

variable "datastore" {
  type        = string
  description = "Datastore name"
  default     = "datastore1"
}

variable "ovf_source" {
  type        = string
  description = "Local path or URL to OVF"
}

variable "network" {
  type        = string
  description = "Network name"
  default     = "VMs"
}
