from .uwsgi_socket import setup_uwsgi_socket
from utils.inquirer_wrapper import get_input

def uwsgi_socket_stream():
    answers = get_input(questions = [
        ("site_name","Application name"),
        ("root_dir","Enter root directory to application"),
    ])

    setup_uwsgi_socket(answers["site_name"], answers["root_dir"])