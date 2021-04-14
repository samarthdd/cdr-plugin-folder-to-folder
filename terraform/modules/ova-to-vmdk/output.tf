output "path" {
  value       = trimprefix(local.vmdk_path, "/vmfs/volumes/${var.datastore}")
  description = "Path to file on ESXi"
}
