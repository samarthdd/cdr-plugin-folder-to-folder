variable "datacenter_id" {
  type        = string
  description = "Datacenter ID"
}

variable "host_id" {
  type        = string
  description = "Host ID"
}

variable "nics" {
  type        = list(string)
  description = "List of NICs to attach"
  default     = ["vmnic0"]
}

variable "switch_name" {
  type        = string
  description = "Switch name"
  default     = "glasswall"
}

variable "port_group_name" {
  type        = string
  description = "PG name"
  default     = "glasswall"
}
