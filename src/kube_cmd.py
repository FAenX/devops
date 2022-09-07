#!/usr/bin/python3.8
import subprocess
import inquirer
import os
import yaml
from utils.config import DevopsConfig


config = DevopsConfig()

def install_minikube_if_not_exists():
    config.create_directories()
    config.create_config_file_if_not_exists()
    minikube_dir = config.minikube_dir
    try:
        subprocess.check_call('docker -v', shell=True)
        
    except:
        subprocess.check_call('apt-get install docker.io -y', shell=True)

    try:
        subprocess.check_call(f'{minikube_dir}/minikube -h > /dev/null', shell=True)
    except:       
        print('executing minikube install')
        subprocess.check_call(f'curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64 && chmod +x minikube-linux-amd64 && mv minikube-linux-amd64 {minikube_dir}/minikube && {minikube_dir}/minikube start', shell=True, cwd=minikube_dir)

    try:
        subprocess.check_call(f'{minikube_dir}/kubectl version --client', shell=True)
    except:
        subprocess.check_call(f'curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl && chmod +x kubectl && mv kubectl {minikube_dir}/', shell=True)



if __name__ == '__main__':
    from run_files.flask import minikube_flask

    install_minikube_if_not_exists()
    
    
    questions = [
    inquirer.Checkbox('stack', message='Choose stack', choices=['wordpress', 'node', 'react', 'flask']),    
    ]

    answers = inquirer.prompt(questions)

    if 'wordpress' in answers['stack']:
        pass
    if 'flask' in answers['stack']:        
        minikube_flask()
        

    