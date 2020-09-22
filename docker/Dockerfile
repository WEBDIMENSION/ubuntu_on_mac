FROM ubuntu:20.04
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
#RUN git clone https://github.com/pyenv/pyenv.git ~/.pyenv
#RUN git clone https://github.com/yyuu/pyenv-virtualenv.git ~/.pyenv/plugins/pyenv-virtualenv
#
#RUN echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc && \
#    echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc && \
#    echo 'eval "$(pyenv init -)"' >> ~/.bashrc && \
#    echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
#
##RUN echo 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.bashrc
#
#RUN apt-get install -y make build-essential libssl-dev zlib1g-dev \
#                       libbz2-dev libreadline-dev libsqlite3-dev wget \
#                       curl llvm libncurses5-dev xz-utils tk-dev \
#                       libxml2-dev libxmlsec1-dev libffi-dev
#
#ENV PATH $PATH:/root/.pyenv/bin
#
#RUN pyenv install 3.7.6 && \
#    pyenv global 3.7.6 && \
#    pyenv rehash
#
#ENV PATH $PATH:/root/.pyenv/shims

#RUN apt-get install libapt-pkg-dev
#RUN pip install --upgrade pip

#RUN apt-get update
#RUN apt-get install -y \
#    openssh-server \
# && rm -rf /var/lib/apt/lists/*
#
RUN mkdir -p /var/run/sshd && chmod 755 /var/run/sshd
#RUN curl -L https://raw.githubusercontent.com/pyenv/pyenv-installer/master/bin/pyenv-installer | bash
#RUN echo $'\n\
#    export PATH="/root/.pyenv/bin:$PATH"\n\
#    eval "$(pyenv init -)"\n\
#    eval "$(pyenv virtualenv-init -)"\n\
#    ' >> /root/.bashrc
#RUN /root/.pyenv/bin/pyenv install 3.7.6
#RUN /root/.pyenv/bin/pyenv global 3.7.6
#RUN /root/.pyenv/bin/pyenv rehash
#RUN /root/.pyenv/shims/python -m pip install --upgrade pip
#
##ARG GITHUB_USER
# ADD ubuntu user, and set password and public key
#ADD https://github.com/${GITHUB_USER}.keys /home/ubuntu/.ssh/authorized_keys
RUN useradd -u 1000 vagrant \
 && usermod -s /bin/bash -G adm,sudo vagrant \
 && echo "vagrant ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers \
 && mkdir -p /home/vagrant

COPY  docker/.ssh/id_rsa /home/vagrant/.ssh/id_rsa
COPY  docker/.ssh/id_rsa.pub /home/vagrant/.ssh/id_rsa.pub
COPY  docker/.ssh/ansible_rsa /home/vagrant/.ssh/ansible_rsa
COPY  docker/.ssh/ansible_rsa.pub /home/vagrant/.ssh/ansible_rsa.pub
COPY  docker/.bashrc /home/vagrant/.bashrc
COPY  docker/.profile /home/vagrant/.profile
RUN   cat /home/vagrant/.ssh/id_rsa.pub >> /home/vagrant/.ssh/authorized_keys
RUN chown -R vagrant.vagrant /home/vagrant
RUN chmod 700 /home/vagrant/.ssh
RUN chmod 600 /home/vagrant/.ssh/*

RUN echo 'root:root' | chpasswd
RUN echo "vagrant:vagrant" | chpasswd
#
EXPOSE 22
CMD [ "/sbin/init" ]
