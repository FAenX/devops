#! /bin/bash

apt update
apt install -y curl gnupg2 software-properties-common apt-transport-https ca-certificates  || echo "Failed to install packages"

(
add-apt-repository ppa:deadsnakes/ppa \
apt install python3.8 python3-pip -y \
&& ln -s /usr/bin/python3.8 /usr/bin/python \
&& pip3 install poetry) || (echo "Python 3.8 not installed" && exit 1)


# install and start nginx
apt install -y nginx || echo "Failed to install nginx"
systemctl start nginx || echo "Failed to start nginx"
# enable nginx
systemctl enable nginx || echo "Failed to enable nginx"

ips=$(hostname -I)
echo $ips

# read ips into an array and pick the first item
read -ra iparr <<< "$ips"

echo "Detected IP:  ${iparr[0]} "

# try to set hostname to ip address catch error if it fails log and continue
echo "setting hostname to ${iparr[0]}"
hostnamectl set-hostname ${iparr[0]} || echo "Failed to set hostname to IP"

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

(curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmour -o /etc/apt/trusted.gpg.d/docker.gpg) \
&& add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" \
|| (echo "Failed to add docker repo" && exit 1)

apt update

(apt install -y containerd.io \
&& containerd config default | sudo tee /etc/containerd/config.toml >/dev/null 2>&1 \
&& systemctl restart containerd \
&& systemctl enable containerd) || (echo "Failed to install containerd" && exit 1)



(curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
apt-add-repository "deb http://apt.kubernetes.io/ kubernetes-xenial main"
) || (echo "Failed to add kubernetes repo" && exit 1)


apt update


apt install -y kubelet kubeadm kubectl
apt-mark hold kubelet kubeadm kubectl

kubeadm init --control-plane-endpoint=$ip  || echo "Error: failed to init kubeadm"
export KUBECONFIG=/etc/kubernetes/admin.conf


curl https://projectcalico.docs.tigera.io/manifests/calico.yaml -O
kubectl apply -f calico.yaml

# install uwsgi
apt install -y  uwsgi || (echo "Failed to install uwsgi" && exit 1)

if -f "/etc/systemd/system/flask.service"
then
    echo "Flask service already exists"
else
    echo "Creating flask service"
(tee /etc/systemd/system/flask.service <<EOF
[Unit]
Description=uWSGI instance to serve flask
After=network.target

[Service]
User=as
Group=www-data
WorkingDirectory=/home/as/flask_app
Environment="PATH=/home/as/flask_app/env/bin"
ExecStart=/home/as/flask_app/venv/bin/uwsgi --ini uwsgi.ini

[Install]
WantedBy=multi-user.target
EOF
) || (echo "Failed to create flask service" && exit 1)
fi

    

systemctl start flask
systemctl enable flask



