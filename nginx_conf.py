#!/usr/bin/env python3

from string import Template
import argparse

# nginx confs string templates
from templates.nginx import nginx_confs
# parse
# terminal argument parser
def parseArgs():
    # create a parser
    parser = argparse.ArgumentParser(description='generate nginx conf.')
    parser.add_argument("--react", action='store_true', help="react with proxy_pass.")
    parser.add_argument("--proxy-conf", action='store_true', help="PROXYserver.")
    parser.add_argument("--jekyll", action='store_true', help="Jekyll")
    parser.add_argument("--static", action='store_true', help="static files.")

    parser.add_argument("servername", help="SERVER_NAME.")
    parser.add_argument("--proxy", help="proxy_pass usr")
    parser.add_argument("--port", help="PORTfor app running on local host for PROXYserver")
    args = parser.parse_args()
    return args


if __name__ == '__main__': 

  args = parseArgs()
  SERVER_NAME = args.servername
  port=3000
  proxy= '127.0.0.1:3000'

  SITE_NAME=SERVER_NAME.split('.')[0]

  if args.proxy:
    PROXY= args.proxy
  if args.port:
    PORT=args.port

  # static server conf
  if args.react:       
    s=nginx_confs.react_conf.safe_substitute(
      SERVER_NAME=SERVER_NAME, 
      PROXY=proxy, 
      SITE_NAME=SITE_NAME
      )
    print(s)
  
  # PROXYserver conf
  if args.proxy_conf:
    s=nginx_confs.proxy_conf.safe_substitute(
      SERVER_NAME=SERVER_NAME, 
      PORT=port
      )

    print(s)

   # static server conf
  if args.static:
    
    s=nginx_confs.static_conf.safe_substitute(
      SERVER_NAME=SERVER_NAME, 
      SITE_NAME=SITE_NAME,
      PORT=port
      )

    print(s)

    # static server conf
  if args.jekyll:
    s=nginx_confs.jekyll_conf.safe_substitute(
      SERVER_NAME=SERVER_NAME, 
      SITE_NAME=SITE_NAME,
      PORT=port
      )

    print(s)