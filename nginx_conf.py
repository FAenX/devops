from string import Template
import argparse
from templates import proxy_to_localhost_nginx_conf, static_server_with_proxy_nginx_conf

# parse
# terminal argument parser
def parseArgs():
    # create a parser
    parser = argparse.ArgumentParser(description='generate nginx conf.')
    parser.add_argument("--static", action='store_true', help="static server with proxy_pass.")
    parser.add_argument("--servername", help="server_name.")
    parser.add_argument("--proxy", help="proxy_pass usr")
    parser.add_argument("--port", help="port for app running on local host for proxy server")
    args = parser.parse_args()
    return args


if __name__ == '__main__': 
  args = parseArgs()
  server_name = args.servername
  port = args.port

  s=proxy_to_localhost_nginx_conf.safe_substitute(server_name=server_name, port=port)
  print(s)