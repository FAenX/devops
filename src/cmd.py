#!/usr/bin/python3.8
import subprocess
import inquirer
import os
import yaml
from utils.config import DevopsConfig
import csv


class Main():
    def __init__(self):
        self.config_instance = DevopsConfig()
        self.config_instance.create_directories_if_not_exists()
        self.config_instance.create_config_file_if_not_exists()
        self.config = self.config_instance.read_config_file()
        self.set_digital_ocean_token()
        self.minikube_dir = self.config.get('minikube_dir')
        self.install_minikube_if_not_exists(self.minikube_dir)


    def set_digital_ocean_token(self):
        print(self.config)
        if not self.config.get('digital_ocean_token'):
            questions = [
                inquirer.Text('token', message="Enter your Digital Ocean token")
            ]
            answers = inquirer.prompt(questions)
            self.config['digital_ocean_token'] = answers['token']
            self.config_instance.update_config_file('digital_ocean_token', answers['token'])

    # check os distro
    def check_os(self):
        if os.path.isfile('/etc/os-release'):
            with open('/etc/os-release') as f:
                reader = csv.reader(f, delimiter="=")
                os_release = dict(reader)
                if os_release['ID'] == 'ubuntu':
                    return 'ubuntu'
                elif os_release['ID'] == 'debian':
                    return 'debian'
                elif os_release.get('ID_LIKE') == 'debian':
                    return 'debian'
                else :
                    return 'unknown'
        else:
            return 'unknown'




    def install_minikube_if_not_exists(self, minikube_dir):
       

        os_check = self.check_os()
        if os_check == 'unknown':
            raise Exception('Unknown OS')


        # if not production use docker else install qemu
        if self.config["production"]:
            # install_qemu()
            pass
        else:
            try:
                subprocess.check_call('docker -v', shell=True)
            
            except:
                subprocess.check_call('apt-get install docker.io -y', shell=True) 
                # enablea nd start docker
                subprocess.check_call('systemctl enable docker', shell=True)


        try:
            subprocess.check_call(f'{minikube_dir}/minikube -h > /dev/null 2>&1', shell=True)
        except Exception as e:     
            # print(e)  
            print('executing minikube install')
            subprocess.check_call(f'curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64 && chmod +x minikube-linux-amd64 && mv minikube-linux-amd64 {minikube_dir}/minikube && {minikube_dir}/minikube start', shell=True, cwd=minikube_dir)

        try:
            subprocess.check_call(f'{minikube_dir}/kubectl version --client', shell=True)
        except:
            subprocess.check_call(f'curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl && chmod +x kubectl && mv kubectl {minikube_dir}/', shell=True)
        try:
            subprocess.check_call('docker-compose -v', shell=True)
        except:
            subprocess.check_call('apt-get install docker-compose -y', shell=True)


        # add minikube to path if not already there
        if not os.environ['PATH'].find(minikube_dir) > -1:
            os.environ['PATH'] = os.environ['PATH'] + ':' + minikube_dir
        


if __name__ == '__main__':
    from run_files.applications import minikube_manifest
    from run_files.wordpress import setup_wordpress_in_docker
    from run_files.applications import flask

   
    # update debian
    subprocess.check_call('apt-get update', shell=True)

    main = Main()
    config = main.config
    

    minikube_dir = config['minikube_dir']

    print(minikube_dir)
    
   
   
    
    
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
        

    