from nginx_to_socket_stream_config import setup_nginx_proxy_to_stream
from uwsgi_socket import setup_uwsgi_socket

def nginx_to_socket_stream__config():
    site_name_or_ip = input("Enter site name or IP: ")
    site_name = input('site name: ')
    root_dir = input('root dir: ')

    setup_nginx_proxy_to_stream(site_name_or_ip, site_name, root_dir)
    setup_uwsgi_socket(root_dir)

if __name__ == '__main__':
    nginx_to_socket_stream__config()
    