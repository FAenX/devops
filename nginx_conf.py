#!/usr/bin/env python3
import sys
import subprocess

import argparse
from string import Template

# nginx confs string templates
from templates.nginx import nginx_confs


# parse
# terminal argument parser
def parseArgs():
    # create a parser
    parser = argparse.ArgumentParser(description='generate nginx conf.')
    parser.add_argument("--react", action='store_true', help="react with proxy_pass.")
    parser.add_argument("--svelte", action='store_true', help="svelte with proxy_pass.")
    parser.add_argument("--docker", action='store_true', help="PROXY server to docker container.")
    parser.add_argument("--jekyll", action='store_true', help="Jekyll")
    parser.add_argument("--static", action='store_true', help="static files.")

    parser.add_argument("servername", help="SERVER_NAME.")
    parser.add_argument("--proxy", help="proxy_pass proxy to ..")
    parser.add_argument("--port", help="PORT for app running on local host for PROXY server")
    args = parser.parse_args()
    return args


if __name__ == '__main__':

  args = parseArgs()
  SERVER_NAME = args.servername
  port=3000
  proxy= '127.0.0.1:3000'

  SITE_NAME=SERVER_NAME.split('.')[0]

  if args.proxy:
    proxy= args.proxy
  if args.port:
    port=args.port

  CACHE_DIRECTIVE = nginx_confs.cache_directive.safe_substitute(SITE_NAME=SITE_NAME)
  CACHE = nginx_confs.cache.safe_substitute(SITE_NAME=SITE_NAME)

  # create cache directory
  command = 'sudo mkdir -p /var/nginx/{0}'.format(SITE_NAME)
  process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
  process.wait()

  if process.returncode == 0:
      print('successfully created folder /var/nginx/{0}'.format(SITE_NAME))
  else:
    sys.exit()

  # static server conf
  if args.react:
    s=nginx_confs.static_common.safe_substitute(
        CACHE_DIRECTIVE=CACHE_DIRECTIVE,
        CACHE=CACHE,
        SERVER_NAME=SERVER_NAME,
        PROXY=proxy,
        SITE_NAME=SITE_NAME,
        DIRECTORY=nginx_confs.dir_react.safe_substitute(SITE_NAME=SITE_NAME)
      )
    print(s)

     # static server conf
  if args.svelte:
    s=nginx_confs.static_common.safe_substitute(
        CACHE_DIRECTIVE=CACHE_DIRECTIVE,
        CACHE=CACHE,
        SERVER_NAME=SERVER_NAME,
        PROXY=proxy,
        SITE_NAME=SITE_NAME,
        DIRECTORY=nginx_confs.dir_svelte.safe_substitute(SITE_NAME=SITE_NAME)
      )
    print(s)


  # PROXYserver conf
  if args.docker:
    s=nginx_confs.reverse_proxy.safe_substitute(
        CACHE_DIRECTIVE=CACHE_DIRECTIVE,
        CACHE=CACHE,
        SERVER_NAME=SERVER_NAME,
        PORT=port
      )

    print(s)

   # static server conf
  if args.static:
    s=nginx_confs.static_common.safe_substitute(
        CACHE_DIRECTIVE=CACHE_DIRECTIVE,
        CACHE=CACHE,
        SERVER_NAME=SERVER_NAME,
        SITE_NAME=SITE_NAME,
        PORT=port,
        DIRECTORY=nginx_confs.dir_static.safe_substitute(SITE_NAME=SITE_NAME)
      )

    print(s)

    # static server conf
  if args.jekyll:
    s=nginx_confs.static_common.safe_substitute(
        CACHE_DIRECTIVE=CACHE_DIRECTIVE,
        CACHE=CACHE,
        SERVER_NAME=SERVER_NAME,
        SITE_NAME=SITE_NAME,
        PORT=port,
        DIRECTORY=nginx_confs.dir_jekyll.safe_substitute(SITE_NAME=SITE_NAME)
      )

    print(s)
