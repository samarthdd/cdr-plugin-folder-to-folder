
output "id" {
  value       = local.id
  description = "File unique ID"
}

output "path" {
  value       = "${local.dirname}/${local.basename}"
  description = "Path to file on ESXi"
}
