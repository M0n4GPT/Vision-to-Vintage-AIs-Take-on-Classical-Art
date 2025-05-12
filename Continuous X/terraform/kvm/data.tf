data "openstack_networking_network_v2" "sharednet2" {
  name = "sharednet2"
}

data "openstack_networking_secgroup_v2" "my_sec_group" {
  name = "my-sec-group35"
}

data "openstack_networking_network_v2" "private_net" {
  name = "private_cloud_net_project35"
}

data "openstack_networking_subnet_v2" "private_subnet" {
  name       = "private_cloud_subnet_project35"
  network_id = data.openstack_networking_network_v2.private_net.id
}
