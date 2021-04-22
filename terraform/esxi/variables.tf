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

variable "ovf_urls" {
  type = object({
    sdk             = string
    workflow        = string
    offline_desktop = string
  })

  description = "URLs to OVAs"
  validation {
    condition     = alltrue([for url in values(var.ovf_urls) : can(regex("https?://.+\\.ov[af]", url))])
    error_message = "URLs have to be valid HTTP/S urls to file ending with .ova or .ovf extention."
  }
}

variable "instance_counts" {
  type = object({
    sdk             = number
    workflow        = number
    offline_desktop = number
  })

  default = {
    workflow        = 1
    sdk             = 2
    offline_desktop = 0
  }

  description = "Count of instances to create"
  validation {
    condition     = alltrue([for n in values(var.instance_counts) : n >= 0])
    error_message = "Count must be >= 0."
  }
}
