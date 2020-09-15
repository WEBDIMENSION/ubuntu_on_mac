# Development environmen for Mac (Ubuntu on mac)
## Required apps (必要アプリ)
- Vagrant
- VMware-Fusion or VirtualBox
- Ubuntu18.04 Image for VMware-Fusion  or VirtualBox
## Purpose 
> Docer for Mac is too late. Create develop (ubuntu18) on mac 
> Install ether tools

## Exec Ansible 
### Case from host
#### Exec all 
```bash
ansible-playbook -i hosts/develop site.yml -l vagrant_ubuntu18
```
#### Tags (specification Tag)
```bash
ansible-playbook -i hosts/develop site.yml -l vagrant_ubuntu18 -t tag
```
#### Skip-tags (Exclusion Tag)
```bash
ansible-playbook -i hosts/develop site.yml -l vagrant_ubuntu18 --skip-tags tag
```
#### Example
ansible-playbook -i hosts/develop site.yml -l vagrant_ubuntu18 -t ansible

### Case Vagrant provisioning
Vagaratfile
```rb
# -*- mode: ruby -*-
# vi: set ft=ruby :

require 'yaml'

if File.file?('vagrant_vmware.yaml')
  settings = YAML.load_file 'vagrant_vmware.yaml'
else
  raise "Configuration file 'vagrant_vmware.yaml' does not exist."
end
#
####################################################
# system command before
####################################################
if settings['system_command_before']
  settings['system_command_before'].each do |i|
    system(i)
  end
end

Vagrant.configure("2") do |config|
  settings['vm'].each do |vm|
    config.vm.define vm['vm_name'] do |v|

      #config.vm.synced_folder ".", "/vagrant", disabled: true
      ####################################################
      # copy files end
      ####################################################

      v.vm.box = vm['box_name']
      v.vm.box_version = vm['box_version']

      #config.vm.box_url =  settings['vm']['boxURL']
      v.disksize.size = vm['disk-space']
      # config.vm.box_check_update = false

      # Create a forwarded port mapping which allows access to a specific port
      # within the machine from a port on the host machine. In the example below,
      # accessing "localhost:8080" will access port 80 on the guest machine.
      # NOTE: This will enable public access to the opened port
      # config.vm.network "forwarded_port", guest: 80, host: 8080

      # Create a forwarded port mapping which allows access to a specific port
      # within the machine from a port on the host machine and only allow access
      # via 127.0.0.1 to disable public access
      # config.vm.network "forwarded_port", guest: 80, host: 8080, host_ip: "127.0.0.1"

      # Create a private network, which allows host-only access to the machine
      # using a specific IP.
      # config.vm.network "private_network", ip: "192.168.33.10"

      #config.vm.network :public_network, :bridge => "en0: HomeWiFi (AirPort)"
      #config.vm.network "private_network", ip: "192.168.33.90"
      if vm['private_network']
        vm['private_network'].each do |i|
          v.vm.network "private_network", ip: i['ip']
        end
      end

      if vm['bridge_network']
        vm['bridge_network'].each do |i|
          v.vm.network :public_network, :bridge => i['name'], ip: i['ip']
          #config.vm.network :public_network, :bridge => i['network_name']
        end
      end

      ####################################################
      # nfs sync  start
      ####################################################
       #vm['sync']['nfs'].any?
      if vm['sync']['nfs']
        vm['sync']['nfs'].each do |i|
        v.vm.synced_folder i['localPath'], i['vmPath'],type: "nfs"
        end
      end
      ####################################################
      # nfs sync  end
      ####################################################

      # Provider-specific configuration so you can fine-tune various
      # backing providers for Vagrant. These expose provider-specific options.
      # Example for VirtualBox:
      #
      v.vm.provider vm['providor'] do |vb|
      #   # Display the VirtualBox GUI when booting the machine
        vb.gui = vm['gui']
        # Customize the amount of memory on the VM:
        vb.memory = vm['memory']
        vb.cpus = vm['cpus']
        #vb.customize ["modifyvm", :id, "--cableconnected1", "on"]
      end

      v.ssh.forward_agent = true

       #config.vm.provision "shell", inline: <<-SHELL
	     # systemctl restart sshd
	     #SHELL

      if settings['system_command']
        settings['system_command'].each do |i|
          system(i)
        end
      end
      if vm['host_name']
         $host_script = "hostnamectl set-hostname " + vm['host_name'].to_s
         v.vm.provision :shell, run: "always", inline: $host_script
       end

      if vm['copyfiles']
        vm['copyfiles'].each do |i|
        v.vm.provision "file", source: i['localPath'], destination: i['vmPath']
        end
      end

      if vm['provision']
        vm['provision'].each do |i|
        v.vm.provision :shell, privileged: false, :path => "provision/"+i
        end
      end
       ####################################################
       #  ansible  start
       ####################################################
      if vm['ansible']
        v.vm.provision vm['ansible']['provision'] do |ansible|
          ansible.verbose            = vm['ansible']['verbose']
          ansible.install            = vm['ansible']['install']
          ansible.install_mode       = vm['ansible']['install_mode']
          ansible.version            = vm['ansible']['version']
          ansible.playbook           = vm['ansible']['playbook']
          ansible.inventory_path     = vm['ansible']['inventory_path']
          ansible.galaxy_roles_path  = vm['ansible']['galaxy_roles_path']
          ansible.limit              = vm['ansible']['limit']
          #ansible.tags = vm['ansible']["tags"], # when need tags. Relation vagrant_vmware.yamal
          #ansible.skip_tags = vm['ansible']["skip_tags"], # when need skip-tags. Relation vagrant_vmware.yamal
        end
      end
       ####################################################
       #  ansible  end
       ####################################################
    end
  end
end
####################################################
# system command after
####################################################
if settings['system_command_after']
  settings['system_command_after'].each do |i|
    system(i)
  end
end

```
vagrant_vmware.yaml
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
  #  develop Vmware Fusion
  ##################################
  - vm_name: "develop"
    box_name: "generic/ubuntu1804"
    box_version: "3.0.12"
    private_network:
      - name: "vm host"
        ip: "192.168.33.10" # Vagrant IP address
    host_name: "develop.local" # Hostname (As you like)
    disk-space: "120GB"  # As you like
    memory: "4096"  # As you like
    cpus: "4" # As you like
    gui: false
    providor: "vmware_fusion" # vmware_fusion or virtualbox
    system_command:
        #- "command"
    sync:
      nfs:  # NFS sync As you like
        - localPath: "../../projects" # As you like
          vmPath: "/home/vagrant/workspace/projects"
        - localPath: "../../develop" # this project !imprtant
          vmPath: "/home/vagrant/workspace/develop"
    copyfiles: # As you like
      - localPath: "~/.ssh/id_rsa"
        vmPath: "~/.ssh/id_rsa"
      - localPath: "~/.ssh/id_rsa.pub"
        vmPath: "~/.ssh/id_rsa.pub"
      - localPath: "~/.ssh/ansible_rsa"
        vmPath: "~/.ssh/ansible_rsa"
      - localPath: "~/.ssh/ansible_rsa.pub"
        vmPath: "~/.ssh/ansible_rsa.pub"
    provision:
      - 'init.sh'
    ansible: # Ansible-setting
      provision: "ansible_local"
      verbose: true
      install: true
      install_mode: "pip"
      version: "2.9.7"
      playbook: "/home/vagrant/workspace/develop/ansible/develop/site.yml" # << Your Ansible playbook
      inventory_path: "/home/vagrant/workspace/develop/ansible/develop/hosts/develop" # << Your Ansible inventory file
      galaxy_roles_path: "/home/vagrant/workspace/develop/ansible/develop/roles" # << Your Ansible roles dir
      limit: "vagrant_ubuntu18" # hostname see  inventoryfile
      # tags: ["tag_name"] # when need tags. Relation Vagrantfile
      # skip_tags: ["tag_name"] # when need tags Relation Vagrantfile
```
UP
```bash
vagrant up develop
```

## Roles
```bash
tree -L 
|-- bash_it
|-- ccze
|-- circleci
|-- common
|-- ctags
|-- develop_init
|-- docker
|-- docker_compose
|-- example
|-- git
|-- glances
|-- gnupg2
|-- goenv
|-- gtags
|-- hostname
|-- jq
|-- lazydocker
|-- luaenv
|-- neofetch
|-- nmap
|-- nodenv
|-- nvim
|-- oh_my_zsh
|-- pass
|-- phpenv
|-- pip
|-- pwgen
|-- pyenv
|-- rbenv
|-- ssh_config
|-- sshpass
|-- tests
|-- tmux
|-- tmuxinator
|-- tmuxp
|-- tree
|-- vim8
|-- zip
`-- zsh
```
## ansible/roles/develop_init is empty and comment out.
This role is use for your personal setting.
Your vimrc, tmux.conf, git clone... more.

## License
MIT

