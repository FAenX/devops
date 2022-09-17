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