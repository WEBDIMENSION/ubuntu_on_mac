[Japanese](https://github.com/WEBDIMENSION/ubuntu_on_mac/blob/master/README_en.md)
# Migrate your development environment to Ubuntu on Mac
![tests](https://github.com/WEBDIMENSION/ubuntu_on_mac/workflows/tests/badge.svg)
![ubuntu](https://img.shields.io/badge/Ubuntu-18.04-green)
![ubuntu](https://img.shields.io/badge/Ubuntu-20.04-green)
![](https://img.shields.io/badge/lint-ansible_lint-green)
![](https://img.shields.io/badge/test-testinfra-green)

## Overview要
Building Ubuntu on a Mac with Vagrant + (VirtualBox or VMware fusion).  
Used Ansible to set up tools for development.


### Purpose
Docker for Mac is too slow, so I want to create a development environment (ubuntu 18 or 20) on a Mac  
and install other development tools to unify the development environment with Ubuntu.  
Use Ansible for environment configuration

### Benefits of Introduction
- Docker works nimbly.
- If the environment is broken, we can rebuild it and restore it.
- Can be developed on Linux (in this case, Ubuntu)
- Easy to rebuild when you buy a new Mac
- Don't mess up your Mac
### Disadvantages of Introduction
- Some knowledge is needed to set up xdebug(php), python interpreter in your editor or IDE.
- Not GUI (DeskTop environment)
- Ubuntu OS Capacity Needed
- CPU utilization may increase when using VirtualBox as a provider (no problem with VMware_fusion)

## Required
- Vagrant
- VMware-Fusion or VirtualBox
- Ubuntu(18.04 or 20.04) Image for VMware-Fusion  or VirtualBox
- Vagrant plugin for VMware

## Sample images
Tmux & Tmuxinator on a Mac connecting to Ubuntu 20.04
![sample_ubuntu20_001](https://user-images.githubusercontent.com/14067241/94424795-c463ec00-01c5-11eb-9677-12969659358f.png)
Running glances on Ubuntu 20.04
![sample_ubuntu20_002](https://user-images.githubusercontent.com/14067241/94425105-4f44e680-01c6-11eb-86e5-738834d904f6.png)

## Operating environment
```bash
Mac 10.15.6 
Vagrant 2.2.9
vmware fusion 11.5.5 
```

## Usage
### Execute Ansible from VM (on Ubuntu)

####  All role executions
```bash
# Ubuntu18.04
ansible-playbook -i hosts/develop site.yml -l vagrant_ubuntu18
# Ubuntu20.04
ansible-playbook -i hosts/develop site.yml -l vagrant_ubuntu20
```
#### Execute with Tag(role)
```bash
# Ubuntu18.04
ansible-playbook -i hosts/develop site.yml -l vagrant_ubuntu18 -t tag
# Ubuntu20.04
ansible-playbook -i hosts/develop site.yml -l vagrant_ubuntu20 -t tag
```
#### Exclude specific tags (role)
```bash
# Ubuntu18.04
ansible-playbook -i hosts/develop site.yml -l vagrant_ubuntu18 --skip-tags tag
# Ubuntu20.04
ansible-playbook -i hosts/develop site.yml -l vagrant_ubuntu20 --skip-tags tag
```

###  Vagrant. In the case of provisioning
Edit the '# As you like' line in vagrant.yml to suit your environment
Reference below

vagrant.yaml
```yml
##################################
#  Before command
##################################
system_command_before:
#- 'touch test.txt'
##################################
#  After command
##################################
system_command_after:
#- 'touch test2.txt'
vm:
  ##################################
  #  Ubuntu Vmware Fusion
  ##################################
  - vm_name: "dev_u18" # As you like
    box_name: "generic/ubuntu1804"
    box_version: "3.0.12"
    private_network:
      - name: "vm host"
        ip: "192.168.33.100" # As you like
#    host_name: "develop.local" # As you like
    disk-space: "50GB" # As you like
    memory: "2048" # As you like
    cpus: "4" # As you like
    gui: false
    providor: "vmware_fusion" # or virtualbox
    system_command:
    #- "command"
    sync:
      nfs: # As you like 
        - localPath: "./ansible"
          vmPath: "/home/vagrant/ansible"
    copyfiles: # As you like
      - localPath: "~/.ssh/id_rsa"
        vmPath: "~/.ssh/id_rsa"
      - localPath: "~/.ssh/id_rsa.pub"
        vmPath: "~/.ssh/id_rsa.pub"
      - localPath: "~/.ssh/ansible_rsa"
        vmPath: "~/.ssh/ansible_rsa"
      - localPath: "~/.ssh/ansible_rsa.pub"
        vmPath: "~/.ssh/ansible_rsa.pub"
    provision_file:
#      - 'init.sh'
    provision_command:
      - "sudo mkdir /vagrant"
      - "sudo chmod 775 /vagrant"
    ansible:
      provision: "ansible_local"
      verbose: true
      install: true
      install_mode: "pip"
      version: "2.9.7"
      playbook: "/home/vagrant/ansible/site.yml"
      inventory_path: "/home/vagrant/ansible/hosts/develop"
      galaxy_roles_path: "/home/vagrant/ansible/roles"
      limit: "vagrant_ubuntu18"
      # tags: [] # when need tags. Relation Vagrantfile
      # skip_tags: [] # when need tags Relation Vagrantfile
  - vm_name: "dev_u20" # As you like
    box_name: "generic/ubuntu2004"
    box_version: "3.0.30"
    private_network:
      - name: "vm host"
        ip: "192.168.33.101" # As you like
    #    host_name: "develop.local" # As you like
    disk-space: "50GB" # As you like
    memory: "2048" # As you like
    cpus: "4" # As you like
    gui: false
    providor: "vmware_fusion" # or virtulabox
    system_command:
    #- "command"
    sync:
      nfs # As you like:
        - localPath: "./ansible"
          vmPath: "/home/vagrant/ansible"
    copyfiles: # As you like
      - localPath: "~/.ssh/id_rsa"
        vmPath: "~/.ssh/id_rsa"
      - localPath: "~/.ssh/id_rsa.pub"
        vmPath: "~/.ssh/id_rsa.pub"
      - localPath: "~/.ssh/ansible_rsa"
        vmPath: "~/.ssh/ansible_rsa"
      - localPath: "~/.ssh/ansible_rsa.pub"
        vmPath: "~/.ssh/ansible_rsa.pub"
    provision_file:
    #      - 'init.sh'
    provision_command:
      - "sudo mkdir /vagrant"
      - "sudo chmod 775 /vagrant"
    ansible:
      provision: "ansible_local"
      verbose: true
      install: true
      install_mode: "pip"
      version: "2.9.7"
      playbook: "/home/vagrant/ansible/site.yml"
      inventory_path: "/home/vagrant/ansible/hosts/develop"
      galaxy_roles_path: "/home/vagrant/ansible/roles"
      limit: "vagrant_ubuntu20"
      # tags: ['example'] # when need tags. Relation Vagrantfile
      # skip_tags: ['example'] # when need tags Relation Vagrantfile
```

Vagrant起動
```bash
vagrant up <vm_name>
```

## Ansible Tasks
Reference: [role directory](https://github.com/WEBDIMENSION/ubuntu_on_mac/tree/master/ansible/roles)

## Commenting out ansible/roles/develop_init.
This role is used in a personal setting.
You can set up your own vimrc, tmux.conf, git clone, etc. as you wish.

## From now on
- [Future Features](https://github.com/WEBDIMENSION/ubuntu_on_mac/labels/enhancement)
- Defective product・feature requests, please contact us.[issue](https://github.com/WEBDIMENSION/ubuntu_on_mac/issues/new)


## License
![](https://img.shields.io/badge/license-MIT-blue)
