from nginx.nginx_to_socket_stream_config import setup_nginx_proxy_to_stream

def nginx_to_socket_stream__config():
    site_name_or_ip = input("Enter site name or IP: ")
    site_name = input('site name: ')
    root_dir = input('root dir: ')
    socket = input('socket: ')

    setup_nginx_proxy_to_stream(site_name_or_ip, site_name, root_dir, socket)

if __name__ == '__main__':
    nginx_to_socket_stream__config()
