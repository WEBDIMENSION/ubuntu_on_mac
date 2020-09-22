#!/usr/bin/env bash
docker rm -f dev
docker rmi dev
docker build -f ubuntu20.04 -t dev .
docker run -itd --privileged  --name dev dev
sleep 10
DOCKER_IP=$(docker inspect --format "{{ .NetworkSettings.IPAddress }}" dev)
echo "IP : "$DOCKER_IP
#ssh vagrant@$DOCKER_IP -p 22 -i $HOME/.ssh/id_rsa "pwd"
ssh vagrant@$DOCKER_IP -i .ssh/ansible_rsa "cd  ~/ansible && \
pip3 install -r requirements.txt && \
source ~/.profile && \
ansible-lint site.yml && \
black && \
flake8 tests && \
ansible-playbook -i hosts/develop site.yml -l vagrant_ubuntu20"
#docker exec -it -u vagrant -w /home/vagrant/ansible dev /bin/bash -c '/exec.sh' --login

