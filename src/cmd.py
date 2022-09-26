#!/usr/bin/python3.8
from curses import flash
import subprocess
import inquirer
from utils.config import DevopsConfig




if __name__ == '__main__':
    # run config
    config = DevopsConfig()
    config = config()

    print(config)

    questions = [
    inquirer.Checkbox('stack', message='Choose stack', choices=['wordpress', 'node', 'react', 'flask','kube-deployment']),    
    ]

    answers = inquirer.prompt(questions)

    if 'wordpress' in answers['stack']:
        print('wordpress')
    if 'flask' in answers['stack']:        
        print('flask')    
    if 'kube-deployment' in answers['stack']:        
        print('kube-deployment')
    if 'node' in answers['stack']:        
        pass
        

    