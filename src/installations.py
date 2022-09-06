#!/usr/bin/env python3
import subprocess
import os


   
def setup_wordpress_in_docker():
    try:
        subprocess.check_call('docker-compose -f src/dockerfiles/wordpress.yml up -d', shell=True)
        print('Wordpress is running')
    except:
        print('Wordpress is not running')
        


