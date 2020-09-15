#!/bin/bash
cp -f ../environment/ssh/id_rsa id_rsa
cp -f ../environment/ssh/id_rsa.pub id_rsa.pub
cp -f ../environment/ssh/ansible_rsa ansible_rsa
cp -f ../environment/ssh/ansible_rsa.pub ansible_rsa.pub
vagrant destroy
vagrant plugin install vagrant-disksize
vagrant plugin install vagrant-global-status
#vagrant plugin install vagrant-vmware-fusion
vagrant plugin install vagrant-vmware-desktop
vagrant plugin license vagrant-vmware-fusion license.lic
vagrant plugin expunge --reinstall
