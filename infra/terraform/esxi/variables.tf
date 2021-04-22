variable "esxi_credentials1" {
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
variable "esxi_credentials2" {
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

variable "instance_counts1" {
  default = {
    workflow        = 1
    sdk             = 2
    offline_desktop = 0
  }
}

variable "instance_counts2" {
  default = {
    workflow        = 0
    sdk             = 4
    offline_desktop = 0
  }
}

variable "ova_source" {
  type = object({
    sdk             = string
    workflow        = string
    offline_desktop = string
  })

  description = "URLs / Local Path to OVAs"

}

variable "sdk_vcpu_count" {
  type        = string
  description = "Count of vCPU per instance"
  default     = "4"

  validation {
    condition     = var.sdk_vcpu_count >= 1
    error_message = "Error: var.sdk_vcpu_count must be >= 1."
  }
}

variable "sdk_memory_mib" {
  type        = number
  description = "Count of RAM per instance in MiB"
  default     = 4096

  validation {
    condition     = var.sdk_memory_mib >= 1024
    error_message = "Error: var.sdk_memory_mib must be >= 1024."
  }
}

variable "sdk_disk_size" {
  type        = number
  description = "disk size"
  default     = 50
}

variable "workflow_vcpu_count" {
  type        = string
  description = "Count of vCPU per instance"
  default     = "2"

  validation {
    condition     = var.workflow_vcpu_count >= 1
    error_message = "Error: var.workflow_vcpu_count must be >= 1."
  }
}

variable "workflow_memory_mib" {
  type        = number
  description = "Count of RAM per instance in MiB"
  default     = 4096

  validation {
    condition     = var.workflow_memory_mib >= 1024
    error_message = "Error: var.workflow_memory_mib must be >= 1024."
  }
}

variable "workflow_disk_size" {
  type        = number
  description = "disk size"
  default     = 50
}

variable "desktop_vcpu_count" {
  type        = string
  description = "Count of vCPU per instance"
  default     = "2"

  validation {
    condition     = var.desktop_vcpu_count >= 1
    error_message = "Error: var.desktop_vcpu_count must be >= 1."
  }
}

variable "desktop_memory_mib" {
  type        = number
  description = "Count of RAM per instance in MiB"
  default     = 4096

  validation {
    condition     = var.desktop_memory_mib >= 1024
    error_message = "Error: var.desktop_memory_mib must be >= 1024."
  }
}

variable "desktop_disk_size" {
  type        = number
  description = "disk size"
  default     = 50
}

variable "network_esxi1" {
  type        = string
  description = "Network name"
  default     = "VMs"
}

variable "datastore_esxi1" {
  type        = string
  description = "Datastore name"
  default     = "datastore1"
}

variable "network_esxi2" {
  type        = string
  description = "Network name"
  default     = "VMs"
}

variable "datastore_esxi2" {
  type        = string
  description = "Datastore name"
  default     = "datastore1"
}

