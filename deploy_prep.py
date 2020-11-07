#!/usr/bin/env python3

import os
import sys
import subprocess
import argparse
import shutil

from templates.node_common.post_receive import common
from templates.nginx.nginx_git_post_receive import restart_nginx
from templates.nginx.react_post_receive import react
from templates.docker.docker_post_receive import docker

# project preparation actions
class Actions:
    def __init__(self, app_name):
        self.DIR_TMP="/srv/tmp/"
        self.DIR_WWW="/srv/www/"
        self.DIR_GIT="/srv/git/"
        self.app_name = app_name   
        self.folders = {'git': '.git', 'www': 'www', 'tmp': 'tmp'}     

    def _dir_create(self, path):        
        command = 'mkdir -p {0}'.format(path)     
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        process.wait()
        if process.returncode == 0:
            return 'created folder {0}'.format(path)
        else:
            error = 'Error code: {}'.format(process.returncode)
            raise Exception(error)
    
    def _own_directory(self, path):
        user = os.getenv('USER')
        # command = 'sudo chown {0} -R {1}'.format(user, os.path.dirname(path))      
        command = 'ls -al {}'.format(os.path.dirname(path))            
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        process.wait()
        
        if process.returncode == 0:
            return 'successfully given ownership to {0} for folder {1}'.format(os.environ['USER'], os.path.dirname(path))
        else:
            error = 'Error code: {}'.format(process.returncode)
            raise ValueError(error)

    def _init_git_repo(self, path):
        command = ['cd {0} & git init --bare --shared=all {0}'.format(path)]
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        process.wait()
        if process.returncode == 0:
            return 'successfully created git bare repo {0}'.format(path)
        return Exception

    def _write_post_receive(self, path, post_receive):
        file_path = '{0}/hooks/post-receive'.format(path)
        with open(file_path, 'w') as f:
            f.writelines(post_receive)  
         
        #  make it executable
        command = 'chmod +x {0}'.format(file_path)
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        process.wait()

        if process.returncode == 0:
            return 'successfully writen file {0}'.format(file_path)
        return Exception

    def _generate_folder_names(self, name):
        # create list of directory paths from app_name
        directories = [
            '{0}{1}.git'.format(self.DIR_GIT, self.app_name),
            '{0}{1}'.format(self.DIR_TMP, self.app_name),
            '{0}{1}'.format(self.DIR_WWW, self.app_name)
            ]
        
        # get git directory from directories
        get_folder_name = lambda y: [x for x in y if '{0}'.format(name) in x]
       
        folder_name=get_folder_name(directories)[0]

        return folder_name


    # actions for priject folders 
    # eg. permissions, mkdir and git init bare
    def folder_actions(self):

        # generate directories
        directories=[
            self._generate_folder_names(folder) for folder in self.folders.values()
            ]
        # give ownership of the directories to current user
        # permisions = [self._own_directory(path) for path in directories]  
        # for i in permisions:     
        #     print('message: {}'.format(i))
            
        # create the directories
        created = [self._dir_create(i) for i in directories]
        for i in created:
            print('message: {}'.format(i))


    # create post receive file
    def git_actions(self, framework, port=3000):
        # initialize bare repo
        git_folder = self._generate_folder_names(self.folders['git'])
        www_folder = self._generate_folder_names(self.folders['www'])
        tmp_folder = self._generate_folder_names(self.folders['tmp'])

        init_git_repo = self._init_git_repo(git_folder)
        
        print('message: {}'.format(init_git_repo))

        # create a post recieve hook in the git repo   
        # for loopback 4 
        if framework == 'node':
            content=common.safe_substitute(
                WWW=www_folder,
                GIT=git_folder,
                TMP=tmp_folder,
                # replace with docker
                DOCKER = docker.safe_substitute(
                    APP_NAME=self.app_name,
                    WWW=www_folder,
                    PORT=port
                ),
                REACT='#',
                NGINX='#'
            )
            print(content)

            post_re = self._write_post_receive(
                git_folder, content)

            print(post_re)


        # for react 
        if framework == 'react':
            content=common.safe_substitute(
                WWW=www_folder,
                GIT=git_folder,
                TMP=tmp_folder,
                REACT = react.safe_substitute(
                    WWW=www_folder,
                ),
                NGINX=restart_nginx,
                DOCKER='#'
            )
            print(content)

            post_re = self._write_post_receive(
                git_folder, content)

            print(post_re)

    def delete(self, app_name):
        paths=[
            self._generate_folder_names(folder) for folder in self.folders.values()
            ]

        # delete project    
        
        commands = ['rm -rf {}'.format(path) for path in paths]
    
        for cmd in commands:
            process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            process.wait()
            # print(process.returncode == 0)
            if process.returncode == 0:
                print('Successfully deleted {}'.format(cmd))
           
        


# terminal argument parser
def parseArgs():
    # create a parser
    parser = argparse.ArgumentParser(description='App options.')
    parser.add_argument("--node", action='store_true', help="Node JS")
    parser.add_argument("--port",  help="host port")
    parser.add_argument("--react", action='store_true', help="React.")
    parser.add_argument("--delete", action='store_true', help="Delete project.")
    parser.add_argument("app_name", metavar=('app_name'), help="Project name.")
    
    return parser.parse_args()



if __name__ == '__main__':
    args = parseArgs()
    # print(args)
    actions = Actions(args.app_name)

    port = 3000
    if args.port:
        port = args.port

    if args.delete:
        actions.delete(args.app_name)
    else:
        actions.folder_actions()

    if args.node:
        actions.git_actions('node', port)
    if args.react:
        actions.git_actions('react')
    

    


    
       
        



