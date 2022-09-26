import subprocess


def  setup_nginx_proxy_to_stream(SERVER_NAME_OR_IP, SITE_NAME, ROOT_DIR, SOCKET):
    "create and nginx configuration"
    config = f'''
    server {{
        listen 80;
        server_name {SERVER_NAME_OR_IP};
        client_max_body_size 50M;
        access_log  /var/log/nginx/$SERVER_NAME.access.log;
        error_log   /var/log/nginx/$SERVER_NAME.error.log;
        location / {{
            include uwsgi_params;
            uwsgi_pass unix:/{ROOT_DIR}/{SOCKET};
        }}
    }}'''

    with open(f'/etc/nginx/sites-available/{SITE_NAME}', 'w') as f:
        f.write(config)

    subprocess.run(['ln', '-s', f'/etc/nginx/sites-available/{SITE_NAME}', f'/etc/nginx/sites-enabled/{SITE_NAME}'])

    subprocess.run(['nginx', '-t'])
    subprocess.run(['systemctl', 'reload', 'nginx'])

