import yaml
import os
from utils.config import DevopsConfig
import subprocess
from templates.git import common_post_receive, various_post_receive
from templates.docker_compose.flask import FlaskProject
from templates.minikube_manifest.manifest import MiniKubeManifest
from utils.config_object import config_object



def minikube_manifest():
    config = config_object()
    project_name = input('Enter project name: ')
    git_dir_path = f"{config['git']}/{project_name}.git"
    project_path = f"{config['projects']}/{project_name}"
    minikube_dir = f"{config['minikube_dir']}"
    subprocess.check_call(f'git init --bare --shared=all {git_dir_path}', shell=True)
   
    content=various_post_receive.minikube.safe_substitute(
        MINIKUBE_DIR=minikube_dir,
        MANIFEST_PATH=f'{project_path}/{project_name}.yml',
        DOCKER_REGISTRY=f'{config["docker_registry"]}',
        APP_NAME=project_name,
        GIT_DIR = git_dir_path,
        APP_DIR = project_path,
        TMP_DIR = f'{config["tmp"]}/{project_name}'
        


       
    )
    print(content)

    with open(f'{git_dir_path}/hooks/post-receive', 'w') as file:
        file.write(content)

    subprocess.check_call(f'chmod +x {git_dir_path}/hooks/post-receive', shell=True)

    flask_project = MiniKubeManifest(project_name)
    flask_project.create_manifest()

    
    


def flask():   
    project_name = input('Enter project name: ')
    port = input('Enter port: ')
    config_path =  DevopsConfig().devops_config_file
    yaml_content = open(f'{config_path}', 'r')
    yaml_content = yaml.load(yaml_content, Loader=yaml.FullLoader)
    git_dir_path = f"{yaml_content['git']}/{project_name}.git"
    project_path = f"{yaml_content['projects']}/{project_name}"
    tempdir = f"{yaml_content['tmp']}/{project_name}"
    subprocess.check_call(f'git init --bare --shared=all {git_dir_path}', shell=True)
   
    content=common_post_receive.common.safe_substitute(
        WWW=project_path,
        GIT=git_dir_path,
        TMP=tempdir,
        # replace with docker
        PLATFORM = various_post_receive.docker.safe_substitute(
            APP_NAME=project_name,
            PORT=port
        ),
    )
    print(content)

    with open(f'{git_dir_path}/hooks/post-receive', 'w') as file:
        file.write(content)

    subprocess.check_call(f'chmod +x {git_dir_path}/hooks/post-receive', shell=True)

    flask_project = FlaskProject(project_name, port)
    flask_project.write_docker_compose_file()



   

