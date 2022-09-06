#!/usr/bin/python3.8
import subprocess
import inquirer


def install_docker_if_not_exists():
    try:
        subprocess.check_call('docker -v', shell=True)
        subprocess.check_call('docker-compose -v', shell=True)
    except:
        subprocess.check_call('apt-get install docker.io -y', shell=True)
        subprocess.check_call('apt-get install docker-compose -y', shell=True)
    
    # mkdir src/.temp if it doesn't exist
    subprocess.check_call('mkdir -p ~/.devops', shell=True)



if __name__ == '__main__':
    from run_files.wordpress import setup_wordpress_in_docker

    install_docker_if_not_exists()
    
    questions = [
    inquirer.Checkbox('stack', message='Choose stack', choices=['wordpress', 'node', 'react']),    
    ]

    answers = inquirer.prompt(questions)

    if 'wordpress' in answers['stack']:
        setup_wordpress_in_docker()
        

    