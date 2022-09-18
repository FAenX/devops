#! /bin/bash

{
hostnamectl set-hostname "127.0.0.1" 
exec bash
}

||{ echo "Error" ; exit 1; }

{

swapoff -a
sed -i '/ swap / s/^\(.*\)$/#\1/g' /etc/fstab
}

||{ echo "Error" ; exit 1; }

{
tee /etc/modules-load.d/containerd.conf <<EOF
overlay
br_netfilter
EOF

}

||{ echo "Error" ; exit 1; }

modprobe overlay
modprobe br_netfilter

{
tee /etc/sysctl.d/kubernetes.conf <<EOF
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
net.ipv4.ip_forward = 1
EOF 

}

||{ echo "Error" ; exit 1; }

{

sysctl --system
    
} ||{ echo "Error" ; exit 1; }

apt install -y curl gnupg2 software-properties-common apt-transport-https ca-certificates
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmour -o /etc/apt/trusted.gpg.d/docker.gpg

add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

apt update
apt install -y containerd.io
containerd config default | sudo tee /etc/containerd/config.toml >/dev/null 2>&1
systemctl restart containerd
systemctl enable containerd
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
apt-add-repository "deb http://apt.kubernetes.io/ kubernetes-xenial main"
apt update
apt install -y kubelet kubeadm kubectl
apt-mark hold kubelet kubeadm kubectl
kubeadm init --control-plane-endpoint='droplet ip'
curl https://projectcalico.docs.tigera.io/manifests/calico.yaml -O
kubectl apply -f calico.yaml
    
    
