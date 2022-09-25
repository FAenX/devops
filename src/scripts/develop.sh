# #! /bin/bash

# apt install -y curl software-properties-common apt-transport-https  || echo "Failed to install packages"

# (apt install \
#     ca-certificates \
#     curl \
#     gnupg \
#     lsb-release) || (echo "Failed to install packages" && exit 1)

# (curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -) || (echo "Failed to add docker repo" && exit 1)
# (add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable") || (echo "Failed to add docker repo" && exit 1)
# (apt-cache policy docker-ce) || (echo "Failed to add docker repo" && exit 1)
# (apt install docker-ce) || (echo "Failed to install  docker" && exit 1)
# (systemctl status docker

# curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
# install minikube-linux-amd64 /usr/local/bin/minikube

# minikube start