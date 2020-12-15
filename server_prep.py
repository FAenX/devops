import os
import sys
import subprocess
import argparse
import shutil
import getpass

def server_prep(): 
    sudoPassword = getpass.getpass('sudo password or blank: ')
    command1 = 'apt update'
    command2 = 'apt-get install nginx'
    command3 = 'curl -fsSL https://get.docker.com -o get-docker.sh'
    command4 = 'sh get-docker.sh'

    os.system('echo %s|sudo -S %s' % (sudoPassword, command1))
    os.system('echo %s|sudo -S %s' % (sudoPassword, command2))
    os.system('echo %s|sudo -S %s' % (sudoPassword, command3))
    os.system('echo %s|sudo -S %s' % (sudoPassword, command4))


if __name__ == '__main__':   
    server_prep()

    # 
