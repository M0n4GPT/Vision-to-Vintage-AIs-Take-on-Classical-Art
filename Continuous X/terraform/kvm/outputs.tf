output "floating_ip" {
  value = openstack_networking_floatingip_v2.floating_ip.address
}

output "private_ips" {
  value = [for p in openstack_networking_port_v2.private_net_ports : p.all_fixed_ips[0]]
}

output "vm_names" {
  value = [for vm in openstack_compute_instance_v2.nodes : vm.name]
}

