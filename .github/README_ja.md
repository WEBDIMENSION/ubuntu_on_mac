[English](README.md)
# Mac上での開発環境をUbuntuへ移行 (Ubuntu on Mac)

![tests](https://github.com/WEBDIMENSION/ubuntu_on_mac/workflows/tests/badge.svg)
![ubuntu](https://img.shields.io/badge/Ubuntu-18.04-green)
![ubuntu](https://img.shields.io/badge/Ubuntu-20.04-green)
![](https://img.shields.io/badge/lint-ansible_lint-green)
![](https://img.shields.io/badge/test-testinfra-green)

## 概要
Mac上でVagrant + ( VirtualBox or VMware fusion ) で Ubuntuを構築。  
開発に必要なツールをAnsibleで構築。


### 経緯
Docker for Macは遅すぎるのでMac上で開発環境(ubuntu18 or 20)を作成し、他の開発ツールもインストールして開発環境をUbuntuに統一したい。  
環境の構成にはAnsibleを使用

### 導入のメリット
- Dockerが軽快に動く
- 環境が壊れたら再構築すれば復旧できる
- Linux上 (この場合はUbuntu) で開発できる
- Mac買い替え時も簡単に再構築
- Mac本体を汚さない
### 導入のデメリット
- xdebug(php), python interpreterをエディタ、IDEに設定する場合は若干知識が必要
- GUI (DeskTop環境ではない)
- Ubuntu OSの容量が必要
- プロバイダにVirtualBox使用時はCPU使用率が上昇する場合あり(VMware_fusionでは問題なし)

## 必要アプリ
- Vagrant
- VMware-Fusion or VirtualBox
- Ubuntu(18.04 or 20.04) Image for VMware-Fusion  or VirtualBox
- Vagrant plugin for VMware

## サンプルイメージ
MacからTmux & Tmuxinator で Ubuntu20.04へ接続
![sample_ubuntu20_001](https://user-images.githubusercontent.com/14067241/94424795-c463ec00-01c5-11eb-9677-12969659358f.png)
Ubuntu20.04上でglances実行
![sample_ubuntu20_002](https://user-images.githubusercontent.com/14067241/94425105-4f44e680-01c6-11eb-86e5-738834d904f6.png)

## 動作環境
```bash
Mac 10.15.6 
Vagrant 2.2.9
vmware fusion 11.5.5 
```

## 使い方
### VM上(Ubuntu上)からAnsible実行

####  全てのrole実行
```bash
# Ubuntu18.04
ansible-playbook -i hosts/develop site.yml -l vagrant_ubuntu18
# Ubuntu20.04
ansible-playbook -i hosts/develop site.yml -l vagrant_ubuntu20
```
#### Tag(role)指定して実行
```bash
# Ubuntu18.04
ansible-playbook -i hosts/develop site.yml -l vagrant_ubuntu18 -t tag
# Ubuntu20.04
ansible-playbook -i hosts/develop site.yml -l vagrant_ubuntu20 -t tag
```
#### 特定タグ(role)を除外して実行
```bash
# Ubuntu18.04
ansible-playbook -i hosts/develop site.yml -l vagrant_ubuntu18 --skip-tags tag
# Ubuntu20.04
ansible-playbook -i hosts/develop site.yml -l vagrant_ubuntu20 --skip-tags tag
```

###  Vagrant プロビジョニングの場合
vagrant.yml の'# As you like' の行を環境にあわせてお好みで編集
下記参考

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
参照: [ロールディレクトリ](https://github.com/WEBDIMENSION/ubuntu_on_mac/tree/master/ansible/roles)

## ansible/roles/develop_init はコメントアウトしています。
このロールは個人的な設定で使用します。
自分のvimrc、tmux.conf、gitクローン等々好きな設定を。

## 今後
- [今後の機能追加](https://github.com/WEBDIMENSION/ubuntu_on_mac/labels/enhancement)
- 不備不具合・機能リクエストとうあれば[イシュー](https://github.com/WEBDIMENSION/ubuntu_on_mac/issues/new)いただけると幸いです。


## ライセンス
![](https://img.shields.io/badge/license-MIT-blue)
