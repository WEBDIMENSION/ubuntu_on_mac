# -*- mode: ruby -*-
# vi: set ft=ruby :

require 'yaml'

if File.file?('vagrant.yaml')
  settings = YAML.load_file 'vagrant.yaml'
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

      config.vm.synced_folder '.', '/vagrant', disabled: true
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

      if vm['private_network']
        vm['private_network'].each do |i|
          v.vm.network "private_network", ip: i['ip']
        end
      end

      if vm['bridge_network']
        vm['bridge_network'].each do |i|
          v.vm.network :public_network, :bridge => i['name'], ip: i['ip']
        end
      end

      ####################################################
      # nfs sync  start
      ####################################################
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
      end

      v.ssh.forward_agent = true

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

      if vm['provision_file']
        vm['provision_file'].each do |i|
        v.vm.provision :shell, privileged: false, :path => "provision/"+i
        end
      end
      if vm['provision_command']
        vm['provision_command'].each do |i|
          v.vm.provision  :shell, inline: i
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
          if vm['ansible']["tags"]
            ansible.tags = vm['ansible']["tags"]
          end

          if vm['ansible']["skip_tags"]
            ansible.tags = vm['ansible']["skip_tags"]
          end
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
