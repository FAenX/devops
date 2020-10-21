from string import Template
import argparse

# nginx confs string templates
from templates import mpesa, nginx

# parse
# terminal argument parser
def parseArgs():
    # create a parser
    parser = argparse.ArgumentParser(description='generate nginx conf.')
    parser.add_argument("--static", action='store_true', help="static server with proxy_pass.")
    parser.add_argument("servername", help="server_name.")
    parser.add_argument("--proxy", help="proxy_pass usr")
    parser.add_argument("--port", help="port for app running on local host for proxy server")
    args = parser.parse_args()
    return args


if __name__ == '__main__': 
  args = parseArgs()
  server_name = args.servername
  port = 3000
  proxy = '127.0.0.1:3000'
  if args.proxy:
    proxy = args.proxy
  if args.port:
    port = args.port

  # static server conf
  if args.static:       
    s=nginx.static_server_with_proxy_nginx_conf.safe_substitute(
      server_name=server_name, 
      proxy=proxy, 
      site_name=server_name
      )
  
  # proxy server conf
  else:
    s=nginx.proxy_to_localhost_nginx_conf.safe_substitute(
      server_name=server_name, 
      port=port
      )

  print(s)