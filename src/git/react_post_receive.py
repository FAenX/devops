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
mkdir -p {tempdir}
mkdir -p {project_path}
git --work-tree={tempdir} --git-dir={git_dir_path} checkout -f || exit;

rm -rf {project_path}/*
cp -r {tempdir}/* {project_path} || exit;
rm -rf {tempdir} || exit;
cd {project_path} || exit;

# create a Dockerfile 
# add multiline string to a file
cat <<EOF > {project_path}/Dockerfile
# Name the node stage "builder"
FROM node:10 AS builder
# Set working directory
WORKDIR /app
# Copy all files from current directory to working dir in image
COPY . .
# install node modules and build assets
RUN npm install && npm run build

# nginx state for serving content
FROM nginx:alpine
# Set working directory to nginx asset directory
WORKDIR /usr/share/nginx/html
# Remove default nginx static assets
RUN rm -rf ./*
# Copy static assets from builder stage
COPY --from=builder /app/build .
# Containers run nginx with global directives and daemon off
ENTRYPOINT ["nginx", "-g", "daemon off;"]
EOF

docker build -t react-nginx .;
docker run -d -p 3002:80 react-nginx --name {project_name};
'''  

    with open(f'{git_dir_path}/hooks/post-receive', 'w') as file:
        file.write(template)

    subprocess.check_call(f'chmod +x {git_dir_path}/hooks/post-receive', shell=True)

    return git_dir_path
    