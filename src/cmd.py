#!/usr/bin/python3.8
import subprocess
import inquirer
from utils.config import DevopsConfig
from utils.install_software import install_all




if __name__ == '__main__':
    from run_files.applications import minikube_manifest
    from run_files.wordpress import setup_wordpress_in_docker
    from run_files.applications import flask
    

    # run config
    config = DevopsConfig()
    config = config()

    print(config)

    install_all()




   
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
        

    