#!/usr/bin/python3.8
import subprocess
import click
import inquirer

def main():
    with subprocess.Popen('\
    apt update && \
    apt install software-properties-common -y  \
    dialog\
    wget\
    python3-pip\
    curl && \
    pip3 install poetry \
    ', 
    shell=True, stdout=subprocess.PIPE) as proc:        
        for line in proc.stdout:
            print(line.decode('utf-8').strip())


if __name__ == '__main__':
    from installations import install_wordpress
    main()

    questions = [
    inquirer.Checkbox('stack', message='Choose stack', choices=['wordpress']),    
    ]

    answers = inquirer.prompt(questions)


    if 'wordpress' in answers['stack']:
        install_wordpress()
        

    