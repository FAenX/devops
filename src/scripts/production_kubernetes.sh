#! /bin/bash

# apt update
# apt install curl -y

ips=$(hostname -I)
echo $ips

# read ips into an array and pick the first item
read -ra iparr <<< "$ips"

echo "Detected IP:  ${iparr[0]} "

# try to set hostname to ip address catch error if it fails log and continue
echo "setting hostname to ${iparr[0]}"
hostnamectl set-hostname ${iparr[0]} || echo "Failed to set hostname to IP"



# exec bash to to apply hostname change
exec bash


# disable swap
echo "Disabling swap"
swapoff -a
sed -i '/ swap / s/^\(.*\)$/#\1/g' /etc/fstab

tee /etc/modules-load.d/containerd.conf <<EOF
overlay
br_netfilter
EOF


modprobe overlay
modprobe br_netfilter

# 
tee /etc/sysctl.d/kubernetes.conf <<EOF
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
net.ipv4.ip_forward = 1
EOF

sysctl --system



# apt install -y curl gnupg2 software-properties-common apt-transport-https ca-certificates

# curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmour -o /etc/apt/trusted.gpg.d/docker.gpg

# ||
# echo "Error: curl -fsSL https://download.docker.com/linux/ubuntu/gpg"
# exit 1




# add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
# ||
# echo "Error: curl -fsSL https://download.docker.com/linux/ubuntu/gpg"
# exit 1





# apt update

# apt install -y containerd.io
# containerd config default | sudo tee /etc/containerd/config.toml >/dev/null 2>&1
# systemctl restart containerd
# systemctl enable containerd
# ||
# echo "Error: apt install -y containerd.io failed"
# echo "exiting"
# exit 1



# curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
# apt-add-repository "deb http://apt.kubernetes.io/ kubernetes-xenial main"
# ||
# echo "Error: curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -"
# echo "exiting"
# exit 1


# apt update


# apt install -y kubelet kubeadm kubectl
# apt-mark hold kubelet kubeadm kubectl
# ||
# echo "Error: apt install -y kubelet kubeadm kubectl"
# echo "exiting"
# exit 1




# kubeadm init --control-plane-endpoint=$ip 
# export KUBECONFIG=/etc/kubernetes/admin.conf


# curl https://projectcalico.docs.tigera.io/manifests/calico.yaml -O
# kubectl apply -f calico.yaml

# ||
# echo "Error: kubeadm init --control-plane-endpoint=$ip"
# echo "exiting"
# exit 1


