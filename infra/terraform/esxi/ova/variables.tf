variable "esxi_credentials" {
  type = object({
    username             = string
    password             = string
    host                 = string
    allow_unverified_ssl = bool
    ssh_port             = number
    ssl_port             = number
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

variable "vcpu_count" {
  type        = string
  description = "Count of vCPU per instance"
  default     = "1"

  validation {
    condition     = var.vcpu_count >= 1
    error_message = "Error: var.vcpu_count must be >= 1."
  }
}

variable "memory_mib" {
  type        = number
  description = "Count of RAM per instance in MiB"
  default     = 1024

  validation {
    condition     = var.memory_mib >= 1024
    error_message = "Error: var.memory_mib must be >= 1024."
  }
}

variable "auto_power_on" {
  type        = bool
  description = "Will power on instances if true"
  default     = false
}

variable "boot_disk_size" {
  type        = number
  description = "HDD size of GiB "
  default     = 0
}

variable "random_string" {
  default = "dev"
}

variable "ip_address" {
  type = string
  description = "IP address to be applied to the instance"
  default = ""
}

variable "gateway_ip" {
  default = "192.168.30.1"
}
