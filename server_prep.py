#!/usr/bin/env python3
import os
import sys
import subprocess
import argparse
import shutil
import getpass
from pymongo import MongoClient

def update():
    command1 = 'apt update' 

    c1 = subprocess.Popen('sudo %s' % (command1), shell=True, stdout=subprocess.PIPE)
    c1.wait()

    if c1.returncode == 0:
        print('updated')
    else:
        print('error updating')


def server_prep():    
    update() 

    docker = subprocess.Popen('docker -v', shell=True, stdout=subprocess.PIPE)
    docker.wait()

    if docker.returncode == 0:
        print('docker already installed')
    else:
        installDocker()

    nginx = subprocess.Popen('nginx -v', shell=True, stdout=subprocess.PIPE)
    nginx.wait()

    if nginx.returncode == 0:
        print('docker already installed')
    else:
        installNginx()
        
    mongo = subprocess.Popen('mongod --version', shell=True, stdout=subprocess.PIPE)
    mongo.wait()

    if mongo.returncode == 0:
        print('mongoDb already installed')
    else:
        installMongoDB()


def installDocker():
    command3 = 'curl -fsSL https://get.docker.com -o get-docker.sh'
    command4 = 'sh get-docker.sh'

    c3 = subprocess.Popen('sudo %s' % (command3), shell=True, stdout=subprocess.PIPE)
    c3.wait()

    c4 = subprocess.Popen('sudo %s' % (command4), shell=True, stdout=subprocess.PIPE)
    c4.wait()

    if c3.returncode == 0:
        print('downloaded install script')
    else:
        sys.exit('error installing docker')

    if c4.returncode == 0:
        print('docker installed')
    else:
        sys.exit('error installing docker')



def installMongoDB():
    m1 = 'wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add -'
    m2 = 'echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/4.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.4.list'
    m3 = 'apt-get install -y mongodb-org'
    # m2 = 'apt-get install gnupg'

    c1 = subprocess.Popen('sudo %s' % (m1), shell=True, stdout=subprocess.PIPE)
    c1.wait()

    if c1.returncode == 0:
        print('imported key from https://www.mongodb.org/static/pgp/server-4.4.asc')
    else:
        sys.exit('error importing key')

    c2 = subprocess.Popen('sudo %s' % (m2), shell=True, stdout=subprocess.PIPE)
    c2.wait()

    if c2.returncode == 0:
        print('created /etc/apt/sources.list.d/mongodb-org-4.4.list file for Ubuntu 20.04')
        update()
    else:
        sys.exit('error creating list')

    c3 = subprocess.Popen('sudo %s' % (m3), shell=True, stdout=subprocess.PIPE)
    c3.wait()

    if c3.returncode == 0:
        print('mongoDB installed')
    else:
        sys.exit('error installing mongoDB')

    mongo_host = input('host: ')

    mongo_port = input('port: ')

    password='T72askY8Am3Yt3Q2'

    client = MongoClient("mongodb://{}:{}".format(mongo_host, mongo_port))

    db = client['admin']

    admin = db.command('createUser', 'mongo-admin', pwd=password, roles=['userAdminAnyDatabase'])
    root = db.command('createUser', 'mongo-root', pwd=password, roles=['root'])

    print(admin)
    print(root)




def installNginx():    
    n = 'apt-get install nginx'

    c2 = subprocess.Popen('sudo %s' % (n), shell=True, stdout=subprocess.PIPE)
    c2.wait()
    if c2.returncode == 0:
        print('nginx installed')
    else:
        sys.exit('error installing')


if __name__ == '__main__':   
    server_prep()

    # 
