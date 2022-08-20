#!/usr/bin/env python3
import subprocess
import os



def install_docker():
    with subprocess.Popen(f'\
    apt install -y docker.io\
    && apt install docker-compose -y \
    ', 
    shell=True, stdout=subprocess.PIPE) as proc:        
        for line in proc.stdout:
            print(line.decode('utf-8').strip())

def install_wordpress():
    install_docker()
    with subprocess.Popen('\
        ls -al && \
        docker-compose -f src/dockerfiles/wordpress.yml up -d\
    ', 
    shell=True, stdout=subprocess.PIPE) as proc:        
        for line in proc.stdout:
            print(line.decode('utf-8').strip())



