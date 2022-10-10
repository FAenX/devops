from utils.config import DevopsConfig
import subprocess
import yaml


# react app post receive
def create_react_post_receive(project_name):
    config_path =  DevopsConfig().devops_config_file
    yaml_content = open(f'{config_path}', 'r')
    yaml_content = yaml.load(yaml_content, Loader=yaml.FullLoader)
    git_dir_path = f"{yaml_content['git']}/{project_name}.git"
    project_path = f"{yaml_content['projects']}/{project_name}"
    tempdir = f"{yaml_content['tmp']}/{project_name}"
    subprocess.check_call(f'git init --bare --shared=all {git_dir_path}', shell=True)

    template = f'''
    # create a post-receive file
    #!/bin/bash
    # generated automatically

    # Deploy the content to the temporary directory
    git --work-tree={tempdir} --git-dir={git_dir_path} checkout -f || exit

    # Replace the content of the production directory
    cd {project_path} || exit
    pwd
    rm -rf .\/* || exit
    mv {tempdir}\/* {project_path} || exit
    npm install
    npm run build
    '''  

    with open(f'{git_dir_path}/hooks/post-receive', 'w') as file:
        file.write(template)

    subprocess.check_call(f'chmod +x {git_dir_path}/hooks/post-receive', shell=True)

    return git_dir_path
    