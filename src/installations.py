#!/usr/bin/env python3
import subprocess
import os



def install_docker():
    with subprocess.Popen(f'\
    curl -fsSL https://get.docker.com -o .get-docker.sh \
    && sh .get-docker.sh \
    ', 
    shell=True, stdout=subprocess.PIPE) as proc:        
        for line in proc.stdout:
            print(line.decode('utf-8').strip())

def install_wordpress():
    install_docker()
    with subprocess.Popen('\
        docker-compose up -d -f dockerfiles/wordpress.yml\
    ', 
    shell=True, stdout=subprocess.PIPE) as proc:        
        for line in proc.stdout:
            print(line.decode('utf-8').strip())



