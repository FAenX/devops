#!/usr/bin/env python3
import sys
import subprocess

import argparse


# nginx confs string templates
import nginx_confs



# parse
# terminal argument parser
def parseArgs():
    # create a parser
    parser = argparse.ArgumentParser(description='generate nginx conf.')
    parser.add_argument("--react", action='store_true', help="react with proxy_pass.")
    parser.add_argument("--svelte", action='store_true', help="svelte with proxy_pass.")
    parser.add_argument("--jekyll", action='store_true', help="Jekyll")
    parser.add_argument("--static", action='store_true', help="static files.")

    parser.add_argument("servername", help="SERVER_NAME.")
    args = parser.parse_args()
    return args


if __name__ == '__main__':

  args = parseArgs()
  SERVER_NAME = args.servername
  port=3000
  proxy= '127.0.0.1:3000'

  SITE_NAME=SERVER_NAME.split('.')[0]

  CACHE_DIRECTIVE = nginx_confs.cache_directive.safe_substitute(SITE_NAME=SITE_NAME)
  CACHE = nginx_confs.cache.safe_substitute(SITE_NAME=SITE_NAME)

  # create cache directory
  command = 'mkdir -p /var/nginx/{0}'.format(SITE_NAME)
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
