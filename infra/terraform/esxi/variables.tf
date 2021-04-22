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
