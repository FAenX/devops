import nginx_confs

def proxy_server(port, SERVER_NAME_IP, CACHE, CACHE_DIRECTIVE):
    """proxy server conf"""
    s = nginx_confs.reverse_proxy.safe_substitute(
        CACHE_DIRECTIVE=CACHE_DIRECTIVE,
        CACHE=CACHE,
        SERVER_NAME=SERVER_NAME_IP,
        PORT=port,
    )

    print(s)

def proxy_to_sream(SERVER_NAME_IP, CACHE, CACHE_DIRECTIVE, ROOT_DIR, SOCKET):
    """proxy server conf"""
    s = nginx_confs.socket_proxy.safe_substitute(
        CACHE_DIRECTIVE=CACHE_DIRECTIVE,
        CACHE=CACHE,
        SERVER_NAME=SERVER_NAME_IP,
        ROOT_DIR=ROOT_DIR,
        SOCKET=SOCKET
    )

    print(s)