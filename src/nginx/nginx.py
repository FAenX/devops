from nginx.nginx_to_socket_stream_config import setup_nginx_proxy_to_stream
from nginx.nginx_to_localhost_and_port_config import setup_nginx_to_localhost
from utils.inquirer_wrapper import get_input

def nginx_to_socket_stream_config():
    answers = get_input(questions = [
        ("server","Enter server IP or domain name"),
        ("site_name","Application name"),
        ("root_dir","Enter root directory to application"),
    ])

    setup_nginx_proxy_to_stream(answers["server"], answers["site_name"], answers["root_dir"])

def nginx_to_localhost_and_port():
    answers = get_input(questions = [
        ("site_name","Application name"),
        ("proxy_pass","Enter url to proxy pass"),
        ('server','Enter server IP or domain name'),
    ])

    setup_nginx_to_localhost(answers["site_name"], answers["server"], answers["proxy_pass"])


class NginXOptions:
    def __init__(self):
        self.options = [
            "nginx_to_socket_stream",
            "nginx_to_localhost_and_port",
        ]

    def get_options(self):
        return self.options




    
    