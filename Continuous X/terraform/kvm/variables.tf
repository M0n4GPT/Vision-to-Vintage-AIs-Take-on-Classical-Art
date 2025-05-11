variable "image_name" {}
variable "flavor_name" {}
variable "key_pair" {}
variable "security_groups" {
  type = list(string)
}
variable "private_fixed_ips" {
  type = list(string)
}
variable "instance_names" {
  type = list(string)
}
variable "floating_ip_existing" {}
variable "floating_ip_pool" {}
