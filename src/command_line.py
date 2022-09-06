#!/usr/bin/python3.8
import subprocess
import inquirer


def install_docker_if_not_exists():
    try:
        subprocess.check_call('docker -v', shell=True)
        print('Docker is already installed')
        subprocess.check_call('docker-compose -v', shell=True)
        print('Docker-compose is already installed')
    except:
        print('Docker is not installed')
        subprocess.check_call('apt-get install docker.io -y', shell=True)
        print('Docker has been installed')
        subprocess.check_call('apt-get install docker-compose -y', shell=True)
        print('Docker-compose has been installed')


if __name__ == '__main__':
    from installations import setup_wordpress_in_docker

    install_docker_if_not_exists()
    
    questions = [
    inquirer.Checkbox('stack', message='Choose stack', choices=['wordpress', 'node', 'react']),    
    ]

    answers = inquirer.prompt(questions)

    if 'wordpress' in answers['stack']:
        setup_wordpress_in_docker()
        

    