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


# check user is root
def check_user_is_root():
    if os.geteuid() != 0:
        raise Exception('You must be root to run this script')

 
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
        subprocess.run(['minikube', 'start', '--driver=none', '--force'])
        # enable minikube addons
    else:
        subprocess.run(['minikube', 'start'])

    subprocess.run(['minikube', 'addons', 'enable', 'ingress'])
    subprocess.run(['minikube', 'addons', 'enable', 'metrics-server'])
    subprocess.run(['minikube', 'addons', 'enable', 'dashboard'])
    subprocess.run(['minikube', 'addons', 'enable', 'registry'])
    subprocess.run(['minikube', 'addons', 'enable', 'storage-provisioner'])
    subprocess.run(['minikube', 'addons', 'enable', 'default-storageclass'])
    subprocess.run(['minikube', 'addons', 'enable', 'ingress-dns'])

# minikube ip
def minikube_ip():
    return subprocess.check_output(['minikube', 'ip']).decode('utf-8').strip()


# setup nginx proxy config
def setup_nginx_proxy():   
    # create nginx config file
    config = read_config_file()
    nginx_config_file = f'''
    server {{
        listen 80;
        server_name {config['domain']};
        location / {{
            proxy_pass http://{minikube_ip()};
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }}
    }}
    '''
    with open('/etc/nginx/sites-available/default', 'w') as f:
        f.write(nginx_config_file)
    subprocess.run(['systemctl', 'restart', 'nginx'])
   

# run all install functions
def install_all():
    if check_os() == 'ubuntu' or check_os() == 'debian':
        check_user_is_root()
        install_docker_if_not_exists()
        install_docker_compose_if_not_exists()
        install_nginx_if_not_exists()
        install_kubectl_if_not_exists()
        install_minikube_if_not_exists()
        
        start_docker_if_not_started()
        start_minikube()
        setup_nginx_proxy()
        
    else: 
        raise Exception('Unknown OS')
   
                
           
