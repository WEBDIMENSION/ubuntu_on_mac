#!/usr/bin/env bash
containers=('ubuntu18.04' 'ubuntu20.04')
for c in "${containers[@]}"
do
docker rm -f $c
docker rmi $c
docker build -f dockerfiles/$c/Dockerfile -t $c .
docker run -itd --privileged  --name $c $c
sleep 10
DOCKER_IP=$(docker inspect --format "{{ .NetworkSettings.IPAddress }}" $c)
echo "IP : "$DOCKER_IP
#ssh vagrant@$DOCKER_IP -p 22 -i $HOME/.ssh/id_rsa "pwd"
ssh vagrant@$DOCKER_IP -i .ssh/ansible_rsa "cd  ~/ansible && \
pip3 install -r requirements.txt && \
source ~/.profile && \
ansible-lint site.yml && \
black && \
flake8 tests && \
ansible-playbook -i hosts/develop site.yml -l $c"
#docker exec -it -u vagrant -w /home/vagrant/ansible dev /bin/bash -c '/exec.sh' --login
done
