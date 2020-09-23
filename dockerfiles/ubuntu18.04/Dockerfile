FROM ubuntu:18.04
RUN apt-get update && \
    apt-get install -y software-properties-common \
                       tzdata

RUN apt-add-repository -y ppa:git-core/ppa && \
    apt-get update && \
    apt-get install -y git \
                       curl \
                       openssh-server \
                       vim \
                       sudo \
                       python3-pip
RUN useradd -u 1000 vagrant \
 && usermod -s /bin/bash -G adm,sudo vagrant \
 && echo "vagrant ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers \
 && mkdir -p /home/vagrant
COPY ansible /home/vagrant/ansible
COPY .ssh/ansible_rsa.pub /home/vagrant/.ssh/ansible_rsa.pub
RUN cat /home/vagrant/.ssh/ansible_rsa.pub >> /home/vagrant/.ssh/authorized_keys
RUN  touch /home/vagrant/.bashrc

RUN echo '\n\
if [ -n "$BASH_VERSION" ]; then\n\
    # include .bashrc if it exists\n\
    if [ -f "$HOME/.bashrc" ]; then\n\
        . "$HOME/.bashrc"\n\
    fi\n\
fi\n\
# set PATH so it includes user's private bin if it exists\n\
if [ -d "$HOME/bin" ] ; then\n\
    PATH="$HOME/bin:$PATH"\n\
fi\n\
# set PATH so it includes user's private bin if it exists\n\
if [ -d "$HOME/.local/bin" ] ; then\n\
    PATH="$HOME/.local/bin:$PATH"\n\
fi\n\
' >> /home/vagrant/.profile

RUN echo '\n\
Host *\n\
    StrictHostKeyChecking no\n\
' >> /home/vagrant/.ssh/config

RUN chown -R vagrant.vagrant /home/vagrant
RUN chmod 700 /home/vagrant/.ssh
RUN chmod 600 /home/vagrant/.ssh/*

RUN echo 'root:root' | chpasswd
RUN echo "vagrant:vagrant" | chpasswd

WORKDIR /home/vagrant/ansible
EXPOSE 22
CMD [ "/sbin/init" ]
