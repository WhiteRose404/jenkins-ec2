variable "instance_type_master" {
    description = "Instance type for master node"
}
variable "instance_type_slave" {
    description = "Instance type for slave node"
}
variable "ami_master" {
    description = "AMI for master node"
}
variable "ami_slave" {
    description = "AMI for slave node"
}
variable "key_pair_path" {
  description = "Path to the SSH key pair used to connect to the EC2 instances"
}
variable "key_pair_name" {
  description = "Name of the SSH key pair used to connect to the EC2 instances"  
}
variable "ingress_rules" {
  description = "List of ingress rules for the security group"
  type = list(object({
    from_port = number
    to_port = number
  }))
}