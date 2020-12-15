import os
import sys
import subprocess
import argparse
import shutil
import getpass


def server_prep():     

    process = subprocess.Popen('docker -v', shell=True, stdout=subprocess.PIPE)
    process.wait()
    if process.returncode == 0:
        print('docker already installed')
    else:
        installDocker()
        
        # os.system('echo %s|sudo -S %s' % (sudoPassword, command4))
        
    
    command1 = 'apt update'
    command2 = 'apt-get install nginx'

    c1 = subprocess.Popen('sudo %s' % (command1), shell=True, stdout=subprocess.PIPE)
    c1.wait()

    c2 = subprocess.Popen('sudo %s' % (command2), shell=True, stdout=subprocess.PIPE)
    c2.wait()
    

    if c1.returncode == 0:
        print('updated')
    else:
        print('error updating')

    if c2.returncode == 0:
        print('nginx installed')
    else:
        sys.exit('error installing')



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
    


if __name__ == '__main__':   
    server_prep()

    # 
