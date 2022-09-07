#!/usr/bin/python3.8
import subprocess
import inquirer
import os
import yaml
from utils.config import DevopsConfig


config = DevopsConfig()

def install_docker_if_not_exists():
    try:
        subprocess.check_call('docker -v', shell=True)
        subprocess.check_call('docker-compose -v', shell=True)
    except:
        subprocess.check_call('apt-get install docker.io -y', shell=True)
        subprocess.check_call('apt-get install docker-compose -y', shell=True)


if __name__ == '__main__':
    from run_files.wordpress import setup_wordpress_in_docker
    from run_files.flask import flask

    install_docker_if_not_exists()
    config.create_directories()
    config.create_config_file_if_not_exists()
    
    questions = [
    inquirer.Checkbox('stack', message='Choose stack', choices=['wordpress', 'node', 'react', 'flask']),    
    ]

    answers = inquirer.prompt(questions)

    if 'wordpress' in answers['stack']:
        setup_wordpress_in_docker()
    if 'flask' in answers['stack']:        
        flask()
        

    