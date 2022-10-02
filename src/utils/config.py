from distutils.command.config import config
import subprocess
import os
import yaml
import inquirer
import csv
import sys
from .inquirer_wrapper import get_input, checbox
import logging

class DevopsConfig:
    def __init__(self, digital_ocean_token=None):
        self.config_file_name = "config.yml"
        self.devops_home = os.path.expanduser("~/.devops")
        self.git = f"{self.devops_home}/git"
        self.www = f"{self.devops_home}/www"
        self.tmp = f"{self.devops_home}/tmp"
        self.projects = f"{self.devops_home}/projects"
        self.devops_config_file = f"{self.devops_home}/{self.config_file_name}"
        self.minikube_dir = f"{self.devops_home}/minikube"
        self.docker_registry = "localhost:5000"
        self.digital_ocean_token = digital_ocean_token
        self.minikube_dir = f"{self.devops_home}/minikube"
        

    def __str__(self):
        return f"Devops config folder: {self.devops_home}"

    # if domain is not set, ask for it and save it to config file
    def get_domain(self):
        config = self.read_config_file()
        if not config.get('domain'):
            questions = [
                inquirer.Text('domain', message="Enter domain name")
            ]
            answers = inquirer.prompt(questions)
            self.update_config_file('domain', answers['domain'])
            return answers['domain']
        else:
            return config['domain']

    # inquire and save environment if not set using list of environments
    def get_environment(self):
        config = self.read_config_file()
        if not config.get('environment'):
            questions = [
                inquirer.List('environment', message="Choose environment", choices=['local', 'development', 'production']),
            ]
            answers = inquirer.prompt(questions)
            self.update_config_file('environment', answers['environment'])
            return answers['environment']
        else:
            return config['environment']
    
    def create_directories_if_not_exists(self):
        os.makedirs(self.devops_home, exist_ok=True)
        os.makedirs(self.git, exist_ok=True)
        os.makedirs(self.tmp, exist_ok=True)
        os.makedirs(self.projects, exist_ok=True)
        os.makedirs(self.minikube_dir, exist_ok=True)
       

    def create_config_file_if_not_exists(self):
        if not os.path.exists(self.devops_config_file):
            with open(self.devops_config_file, 'w') as file:
                documents = yaml.dump(self.__dict__(), file)
                print(documents)

    def read_config_file(self):
        self.create_config_file_if_not_exists()
        with open(self.devops_config_file, 'r') as file:
            return yaml.load(file, Loader=yaml.FullLoader)

    def update_config_file(self, key, value):
        config = self.read_config_file()
        config[key] = value
        with open(self.devops_config_file, 'w') as file:
            documents = yaml.dump(config, file)
            print(documents)

    def set_digital_ocean_token(self):
        config = self.read_config_file()
        if not config.get('digital_ocean_token'):        
            questions = [
                inquirer.Text('token', message="Enter your Digital Ocean token")
            ]
            answers = inquirer.prompt(questions)
            self.digital_ocean_token = answers['token']
            self.update_config_file('digital_ocean_token', answers['token'])
    
    def software_dependencies(self):
        config = self.read_config_file()
        answers = {'software_dependencies': []}
        if not config.get('software_dependencies'):
            answers = checbox(options=['nginx'], message='Choose software dependencies', name='software_dependencies')
            print(answers)

            # check if nginx is already installed and if not install it
        if 'nginx' in answers['software_dependencies']:
            try:
                subprocess.check_call(['nginx', '-v'])
            except:
                subprocess.check_call(['apt', 'install', 'nginx', '-y'])                 

            self.update_config_file('software_dependencies', answers)
            

   
    def __call__(self):
        self.create_directories_if_not_exists()
        self.create_config_file_if_not_exists()        
        self.set_digital_ocean_token()
        self.get_environment()
        self.get_domain()
        self.software_dependencies()
    
    def __dict__(self):
        return {
            "git": self.git,
            "www": self.www,
            "tmp": self.tmp,
            "devops_config_file": self.devops_config_file,
            "devops_home": self.devops_home,
            "config_file_name": self.config_file_name,
            "projects": self.projects,
            "docker_registry": self.docker_registry,
            "minikube_dir": self.minikube_dir,
        }