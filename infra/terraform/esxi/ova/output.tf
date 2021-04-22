output "esxi_guest" {
  value       = esxi_guest.this
  description = "Guests objects"
}

output "ipv4" {
  value       = [for vm in esxi_guest.this : vm.ip_address]
  description = "IPv4 addresses of all instances"
}

output "map" {
  value = {
    for vm in esxi_guest.this :
    vm.guest_name => {
      ip_address     = vm.ip_address
      ovf_source     = vm.ovf_source
      guestos        = vm.guestos
      vcpu_count     = vm.numvcpus
      memory_mib     = vm.memsize
      boot_disk_size = coalesce(vm.boot_disk_size, "Default from OVA/OVF")
    }
  }
  description = "Rish map with information"
}
