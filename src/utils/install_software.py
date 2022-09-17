import os 
import sys
import csv
import subprocess
import yaml
from .config import DevopsConfig

# read config file
def read_config_file():
    config = DevopsConfig()
    return config.read_config_file()

# check os distro
def check_os():
    if os.path.isfile('/etc/os-release'):
        with open('/etc/os-release') as f:
            reader = csv.reader(f, delimiter="=")
            os_release = dict(reader)
            if os_release['ID'] == 'ubuntu':
                return 'ubuntu'
            elif os_release.get('ID_LIKE') == 'debian':
                return 'debian'
            else :
                return 'unknown'
    else:
        return 'unknown'


# check user is root
def check_user_is_root():
    if os.geteuid() != 0:
        raise Exception('You must be root to run this script')

# install kvm if user is root and environment is production and os is ubuntu or debian
def install_kvm_if_not_exists():
    # if kvm already installed do nothing
    config = read_config_file()
    if os.path.isfile('/dev/kvm'):
        return   

    if config['environment'] != 'production':
        return
   
    subprocess.run(['apt-get', 'update'])
    subprocess.run(['apt-get', 'install', 'qemu-kvm', 'libvirt-daemon-system', 'libvirt-clients', 'bridge-utils', 'virtinst', 'virt-manager', 'libguestfs-tools', '-y'])
    subprocess.run(['systemctl', 'enable', 'libvirtd'])
    subprocess.run(['systemctl', 'start', 'libvirtd'])
 
# install minikube if user is root and os is ubuntu or debian
def install_minikube_if_not_exists():
    # if minikube already installed do nothing
    minikube_dir = read_config_file()['minikube_dir']

    try:
        subprocess.run(['minikube', 'version'])
        return
    except:
        # print(e)  
        print('executing minikube install')
        subprocess.check_call(f'curl -LO \
        https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64 \
        && chmod +x minikube-linux-amd64 \
        && mv minikube-linux-amd64 {minikube_dir}/minikube', shell=True, cwd=minikube_dir)
        
       

    
# install kubectl if user is root and os is ubuntu or debian
def install_kubectl_if_not_exists():
    minikube_dir = read_config_file()['minikube_dir']
    try:
        subprocess.run(['kubectl', '--version'])
        return
    except:        
        subprocess.check_call(f'curl -LO \
            https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl \
            && chmod +x kubectl && mv kubectl {minikube_dir}/', shell=True)
            # add kubectl to path
       


    

# install docker if user is root and os is ubuntu or debian
def install_docker_if_not_exists():
    # if docker already installed do nothing
    try:
        subprocess.run(['docker', '--version'])
        return
    except:
        subprocess.run(['apt-get', 'update'])
        subprocess.run(['apt-get', 'install', 'docker.io', '-y'])
     
# install docker-compose if user is root and os is ubuntu or debian
def install_docker_compose_if_not_exists():
    try:
        subprocess.run(['docker-compose', '--version'])
        return
    except:    
        subprocess.run(['apt-get', 'install', 'docker-compose', '-y'])    
       
       
# install nginx if user is root and os is ubuntu or debian
def install_nginx_if_not_exists():
    # if nginx already installed do nothing
    try:
        subprocess.run(['nginx', '-v'])
        return
    except:        
        subprocess.run(['apt-get', 'update'])
        subprocess.run(['apt-get', 'install', 'nginx', '-y'])
        subprocess.run(['systemctl', 'enable', 'nginx'])
        subprocess.run(['systemctl', 'start', 'nginx'])
       
# start docker if environment is development
def start_docker_if_not_started():
    config = read_config_file()
    if config['environment'] == 'development':
        try:
            subprocess.run(['docker', '--version'])
            subprocess.run(['systemctl', 'start', 'docker'])
            subprocess.run(['systemctl', 'enable', 'docker'])
        except:
            raise Exception('Docker not installed')

# start minikube with kvm if environment == production or staging
def start_minikube():
    config = read_config_file()
    if config['environment'] == 'production' or config['environment'] == 'staging':
        subprocess.run(['minikube', 'start', '--driver=kvm2', '--force'])
        # enable minikube addons
        subprocess.run(['minikube', 'addons', 'enable', 'ingress'])
        subprocess.run(['minikube', 'addons', 'enable', 'metrics-server'])
        subprocess.run(['minikube', 'addons', 'enable', 'dashboard'])
        subprocess.run(['minikube', 'addons', 'enable', 'registry'])
        subprocess.run(['minikube', 'addons', 'enable', 'storage-provisioner'])
        subprocess.run(['minikube', 'addons', 'enable', 'default-storageclass'])
        subprocess.run(['minikube', 'addons', 'enable', 'ingress-dns'])
    else:
        subprocess.run(['minikube', 'start'])

# run all install functions
def install_all():
    if check_os() == 'ubuntu' or check_os() == 'debian':
        check_user_is_root()
        install_docker_if_not_exists()
        install_docker_compose_if_not_exists()
        install_nginx_if_not_exists()
        install_kubectl_if_not_exists()
        install_minikube_if_not_exists()
        install_kvm_if_not_exists()
        start_docker_if_not_started()
        start_minikube()
    else: 
        raise Exception('Unknown OS')
   
                
           
