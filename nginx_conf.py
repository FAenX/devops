from string import Template
from templates import proxy_to_localhost_nginx_conf

# nginx file


if __name__ == '__main__': 
  path = '/etc/nginx/sites-available'
  port = 3004
  server_name = 'https://valueads-api.touchinspiration.net'

  s=proxy_to_localhost_nginx_conf.safe_substitute(server_name=server_name, port=port)
  print(s)