variable "image_name" {}
variable "flavor_name" {}
variable "key_pair" {}
variable "security_groups" {}
variable "private_fixed_ips" {
  type = list(string)
}
variable "instance_names" {
  type = list(string)
}
variable "floating_ip_existing" {
  default = "129.114.25.100"
}
variable "floating_ip_pool" {}

data "openstack_networking_network_v2" "private_net" {
  name = "private"
}

data "openstack_networking_network_v2" "shared_net" {
  name = "sharednet1"
}

data "openstack_networking_subnet_v2" "private_subnet" {
  name = "private-subnet"
}

resource "openstack_networking_port_v2" "private_port" {
  count          = 3
  name           = "project35-port-${count.index}"
  network_id     = data.openstack_networking_network_v2.private_net.id

  fixed_ip {
    ip_address = var.private_fixed_ips[count.index]
    subnet_id  = data.openstack_networking_subnet_v2.private_subnet.id
  }

  admin_state_up        = true
  port_security_enabled = false
}

resource "openstack_networking_port_v2" "shared_port" {
  count          = 3
  name           = "sharednet-port-${count.index}"
  network_id     = data.openstack_networking_network_v2.shared_net.id
  admin_state_up = true
}

resource "openstack_compute_instance_v2" "vm_instance" {
  count          = 3
  name           = var.instance_names[count.index]
  image_name     = var.image_name
  flavor_name    = var.flavor_name
  key_pair       = var.key_pair
  security_groups = var.security_groups

  network {
    port = openstack_networking_port_v2.private_port[count.index].id
  }

  network {
    port = openstack_networking_port_v2.shared_port[count.index].id
  }
}

# Associate ONLY node1 (index 0) with the floating IP
resource "openstack_networking_floatingip_associate_v2" "fip_assoc_node1" {
  floating_ip = var.floating_ip_existing
  port_id     = openstack_networking_port_v2.shared_port[0].id
}
