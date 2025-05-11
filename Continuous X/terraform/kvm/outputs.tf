output "floating_ip" {
  description = "The floating IP assigned to node-1-project35"
  value       = openstack_networking_floatingip_associate_v2.fip_assoc_node1.floating_ip
}

output "private_ips" {
  description = "Fixed private IPs for all VMs"
  value       = [for p in openstack_networking_port_v2.private_port : p.fixed_ip[0].ip_address]
}

output "vm_names" {
  description = "Names of all provisioned VMs"
  value       = [for vm in openstack_compute_instance_v2.vm_instance : vm.name]
}
