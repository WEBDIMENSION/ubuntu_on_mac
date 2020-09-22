#!/usr/bin/env bash
docker rm -f dev
#docker rmi dev
#docker build . -t dev
cp -rf ~/.ssh ./.ssh
docker run -itd --privileged -v /home/vagrant/workspace/develop/ansible/Develop_on_ubuntu/ansible:/home/vagrant/ansible  -p 2223:22 --name dev dev
sleep 10
DOCKER_IP=$(docker inspect --format "{{ .NetworkSettings.IPAddress }}" dev)
echo "IP : "$DOCKER_IP
echo "ssh vagrant@$DOCKER_IP -i $HOME/.ssh/id_rsa"
#ssh vagrant@$DOCKER_IP -p 22 -i $HOME/.ssh/id_rsa "pwd"
ssh vagrant@$DOCKER_IP -i ~/.ssh/id_rsa "cd  ~/ansible && \
pip3 install -r requirements.txt && \
source ~/.profile && \
ansible-playbook -i hosts/develop site.yml -l vagrant_ubuntu20"
#docker exec -it -u vagrant -w /home/vagrant/ansible dev /bin/bash -c '/exec.sh' --login

