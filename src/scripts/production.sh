#! /bin/bash

apt update
apt install python3-pip -y \
|| echo "Failed to install python3 and python3-pip" 

pip3 install poetry \
&& poetry config virtualenvs.in-project true || echo "Failed to install poetry"

apt install -y curl gnupg2 software-properties-common apt-transport-https ca-certificates  || echo "Failed to install packages"


# install and start nginx
apt install -y nginx || echo "Failed to install nginx"
systemctl start nginx || echo "Failed to start nginx"
# enable nginx
systemctl enable nginx || echo "Failed to enable nginx"

# ips=$(hostname -I)
# echo $ips

# # read ips into an array and pick the first item
# read -ra iparr <<< "$ips"

# echo "Detected IP:  ${iparr[0]} "

# try to set hostname to ip address catch error if it fails log and continue
echo "setting hostname to kube-master"
hostnamectl set-hostname 'kube-master' || echo "Failed to set hostname to IP"

# disable swap
echo "Disabling swap"
swapoff -a && sed -i '/ swap / s/^\(.*\)$/#\1/g' /etc/fstab || echo "Failed to disable swap"


tee /etc/modules-load.d/containerd.conf <<EOF
overlay
br_netfilter
EOF

modprobe overlay && modprobe br_netfilter || echo "Failed to load modules"

# 
tee /etc/sysctl.d/kubernetes.conf <<EOF
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
net.ipv4.ip_forward = 1
EOF

sysctl --system

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmour -o /etc/apt/trusted.gpg.d/docker.gpg \
&& add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" \
|| (echo "Failed to add docker repo" && exit 1)

apt update

apt install -y containerd.io containerd docker.io
&& containerd config default | tee /etc/containerd/config.toml >/dev/null 2>&1 \
&& systemctl restart containerd \
&& systemctl enable containerd || echo "Failed to install containerd" 



curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
apt-add-repository "deb http://apt.kubernetes.io/ kubernetes-xenial main"
|| (echo "Failed to add kubernetes repo" && exit 1)


apt update


apt install -y kubelet kubeadm kubectl
apt-mark hold kubelet kubeadm kubectl

kubeadm init --control-plane-endpoint='kube-master' --ignore-preflight-errors=all -v=9 || echo "Error: failed to init kubeadm"
export KUBECONFIG=/etc/kubernetes/admin.conf


curl https://projectcalico.docs.tigera.io/manifests/calico.yaml -O
kubectl apply -f calico.yaml

# install uwsgi
apt install -y  uwsgi || (echo "Failed to install uwsgi" && exit 1)





