provider "aws" {
    region = "eu-west-3"
}

locals {
    sg_protocol = "tcp"
    sg_cidr = ["0.0.0.0/0"]
}

resource "aws_security_group" "allow_ssh" {
    name = "allow_ssh"
    description = "Allow SSH inbound traffic"
    
    dynamic "ingress" {
        for_each = var.ingress_rules
        content {
            from_port = ingress.value.from_port
            to_port = ingress.value.to_port
            protocol = local.sg_protocol
            cidr_blocks = local.sg_cidr
        }
    }
    egress {
        from_port = 0
        to_port = 0
        protocol = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }
}

resource "aws_instance" "master" {
    ami = var.ami_master
    instance_type = var.instance_type_master
    key_name = var.key_pair_name
    tags = {
        Name = "jenkins-master"
    }
}

resource "aws_instance" "slave" {
    count = 3
    ami = var.ami_slave
    instance_type = var.instance_type_slave
    key_name = var.key_pair_name
    tags = {
        Name = "jenkins-slave-${count.index}"
    }
}

resource "null_resource" "update_yml" {
    depends_on = [ aws_instance.master, aws_instance.slave ]
    provisioner "local-exec" {
        command = "echo '${templatefile("template/inventory.tftpl", {
            master_ip = aws_instance.master.public_ip
            slaves = aws_instance.slave
            host = "ubuntu"
            key_pair_path = var.key_pair_path
        })}' > ../ansible/inventory.yml"
    }
}