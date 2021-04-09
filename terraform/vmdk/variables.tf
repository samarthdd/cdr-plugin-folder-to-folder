variable "name_prefix" {
  type        = string
  description = "Name prefix for autonaming"
  default     = "instance"

  validation {
    condition     = can(regex("^[a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9]$", var.name_prefix))
    error_message = "Name prefix must match ^[a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9]$."
  }
}

variable "vmdk" {
  type        = string
  description = "Path to VMDK in the datastore"
}

variable "guest_id" {
  type        = string
  description = "Instance guest ID"
  default     = "otherLinux64Guest"
}

variable "cpu" {
  type        = number
  description = "Count of vCPU"
  default     = 1

  validation {
    condition     = var.cpu >= 1
    error_message = "Number of CPU must be >= 1."
  }
}

variable "ram" {
  type        = number
  description = "Quantity of RAM in MiB"
  default     = 1024

  validation {
    condition     = var.ram >= 1024
    error_message = "Quantity of RAM in MiB must be >= 1024."
  }
}

variable "instance_count" {
  type        = number
  description = "Number of instances to create"
  default     = 1

  validation {
    condition     = var.instance_count >= 1
    error_message = "Number of instances to create must be >= 1."
  }
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

variable "wait_for_guest_net_timeout" {
  type        = number
  description = "Timeout it seconds"
  default     = 0
  validation {
    condition     = var.wait_for_guest_net_timeout >= 0
    error_message = "Timeout it seconds must be >= 0."
  }
}

variable "wait_for_guest_ip_timeout" {
  type        = number
  description = "Timeout it seconds"
  default     = 0
  validation {
    condition     = var.wait_for_guest_ip_timeout >= 0
    error_message = "Timeout it seconds must be >= 0."
  }
}

variable "data" {
  type = object({
    pool_id        = string
    datastore_name = string
    datastore_id   = string
    host_id        = string
    network_id     = string
  })
  description = "Data from module data"
}
