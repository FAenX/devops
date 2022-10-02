#!/usr/bin/python3.8
from curses import flash
import subprocess
import inquirer
from utils.config import DevopsConfig
from utils.inquirer_wrapper import get_input, checbox
from nginx.nginx import NginXOptions, nginx_to_localhost_and_port, nginx_to_socket_stream_config
import logging
from socket_stream.socket_stream import uwsgi_socket_stream




if __name__ == '__main__':
    # run config
    config = DevopsConfig()
    config = config()

    print(config)

    answers = checbox(['wordpress', 'node', 'react', 'flask','kube-deployment', 'nginx', 'uwsgi socket stream'], message='Choose the application stack', name='stack')

    print(answers)

    if 'nginx' in answers['stack']:
        nginx_options = NginXOptions()
        answers = checbox(nginx_options.get_options(), message='Choose nginx option', name='nginx_option')
        if 'nginx_to_socket_stream' in answers['nginx_option']:
            nginx_to_socket_stream_config()
        elif 'nginx_to_localhost_and_port' in answers['nginx_option']:
            nginx_to_localhost_and_port()

    if 'uwsgi socket stream' in answers['stack']:
        uwsgi_socket_stream()
            

        



   

   

    

    