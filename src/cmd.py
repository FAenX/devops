#!/usr/bin/python3.8
import subprocess
import inquirer
import os
import yaml
from utils.config import DevopsConfig
import csv



config_instance = DevopsConfig()
config = config_instance.config
minikube_dir = config.get('minikube_dir')


if __name__ == '__main__':
    from run_files.applications import minikube_manifest
    from run_files.wordpress import setup_wordpress_in_docker
    from run_files.applications import flask
    # update debian
    subprocess.check_call('apt-get update', shell=True)

    print(minikube_dir)
    questions = [
    inquirer.Checkbox('stack', message='Choose stack', choices=['wordpress', 'node', 'react', 'flask','kube-deployment']),    
    ]

    answers = inquirer.prompt(questions)

    if 'wordpress' in answers['stack']:
        setup_wordpress_in_docker()
    if 'flask' in answers['stack']:        
        flask()        
    if 'kube-deployment' in answers['stack']:        
        minikube_manifest()
    if 'node' in answers['stack']:        
        pass
        

    