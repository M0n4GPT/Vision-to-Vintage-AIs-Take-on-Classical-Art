# Lookup private network
data "openstack_networking_network_v2" "private_net" {
  name = "private_cloud_net_project35"
}

# Lookup shared/public network
data "openstack_networking_network_v2" "shared_net" {
  name = "sharednet1"
}

# Lookup subnet from private network
data "openstack_networking_subnet_v2" "private_subnet" {
  name       = "private_cloud_subnet_project35"
  network_id = data.openstack_networking_network_v2.private_net.id
}
