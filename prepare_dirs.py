import os
import sys
import subprocess
import argparse

from templates import git_post_recieve

class DirectoryFuncs:
    def __init__(self, app_name):
        self.DIR_TMP="/srv/tmp/"
        self.DIR_WWW="/srv/www/"
        self.DIR_GIT="/srv/git/"
        self.app_name = app_name

    def generate_dirs(self):    
        return [
            '{0}{1}.git'.format(self.DIR_GIT, self.app_name),
            '{0}{1}'.format(self.DIR_TMP, self.app_name),
            '{0}{1}'.format(self.DIR_WWW, self.app_name)
            ]

    def dir_create(self, path):        
        command = 'sudo mkdir -p {0}'.format(path)     
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        process.wait()
        return process.returncode
    
    def own_directory(self, path):
        user = os.getenv('USER')
        command = 'sudo chown {0} -R {1}'.format(user, path)     
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        process.wait()
        return process.returncode

    def init_git_repo(self, path):
        command = 'cd {0} & git init --bare --shared=all {0}'.format(path)
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        process.wait()
        return process.returncode

    def write_post_receive(self, path, post_receive):
        return post_receive.safe_substitute(
            WWW=self.DIR_WWW
        )


# terminal argument parser
def parseArgs():
    # create a parser
    parser = argparse.ArgumentParser(description='App options.')
    parser.add_argument("--lb4", action='store_true', help="Loopback 4.")
    parser.add_argument("--lb3", action='store_true', help="Loopback 3.")
    parser.add_argument("--react", action='store_true', help="React.")

    args = parser.parse_args()
    return args



if __name__ == '__main__':
    args = parseArgs()

     # get git directory from directories
    get_git_dir = lambda y: [x for x in y if '.git' in x]

     # get www directory from directories
    get_www_dir = lambda y: [x for x in y if 'www' in x]

     # get tmp directory from directories
    get_tmp_dir = lambda y: [x for x in y if 'tmp' in x]
    

    # init class
    directoryFuncs=DirectoryFuncs('test-app')

    # create list of directory paths from app_name
    directories = directoryFuncs.generate_dirs()
    print(directories)

    # generate directory path names
    git_dir=get_git_dir(directories)[0]
    tmp_dir=get_tmp_dir(directories)[0]
    www_dir=get_www_dir(directories)[0]

    # create the directories
    created = [directoryFuncs.dir_create(i) for i in directories]
    print(created)

    # give ownership of the directories to current user
    permisions = [directoryFuncs.own_directory(i) for i in directories]
    print(permisions)

    
    
    # initialize bare repo
    
    git_repo = directoryFuncs.init_git_repo(git_dir)
    print(git_repo)

    # create a post recieve hook in the git repo    
    if args.lb4:
        content=git_post_recieve.post_recieve_common.safe_substitute(
            WWW=www_dir,
            GIT=git_dir,
            TMP=tmp_dir
        )
        print(content)

        # post_re = directoryFuncs.write_post_receive(
        #     git_dir, )

        # print(post_re)


