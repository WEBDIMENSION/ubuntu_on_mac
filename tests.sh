#!/usr/bin/env bash
docker rm -f ubuntu18.04
docker rmi ubuntu20.04
docker build -f dockerfiles/ubuntu20.04/Dockerfile -t ubuntu20.04 .
docker run -itd --privileged  --name ubuntu20.04 ubuntu20.04
sleep 10
DOCKER_IP=$(docker inspect --format "{{ .NetworkSettings.IPAddress }}" ubuntu20.04)
echo "IP : "$DOCKER_IP
#ssh vagrant@$DOCKER_IP -p 22 -i $HOME/.ssh/id_rsa "pwd"
ssh vagrant@$DOCKER_IP -i .ssh/ansible_rsa "cd  ~/ansible && \
pip3 install -r requirements.txt && \
source ~/.profile && \
ansible-lint site.yml && \
black && \
flake8 tests && \
ansible-playbook -i hosts/develop site.yml -l ubuntu20.04"
#docker exec -it -u vagrant -w /home/vagrant/ansible dev /bin/bash -c '/exec.sh' --login

