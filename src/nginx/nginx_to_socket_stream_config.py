import subprocess


def  setup_nginx_proxy_to_stream(server, site_name, root_dir):
    "create and nginx configuration"
    config = f'''
    server {{
        server_name {server};
        client_max_body_size 50M;
        access_log  /var/log/nginx/{server}.access.log;
        error_log   /var/log/nginx/{server}.error.log;
        location / {{
            include uwsgi_params;
            uwsgi_pass unix:/{root_dir}/{site_name}.sock;
        }}
    }}'''

    with open(f'/etc/nginx/sites-available/{site_name}', 'w') as f:
        f.write(config)

    subprocess.run(['ln', '-s', f'/etc/nginx/sites-available/{site_name}', f'/etc/nginx/sites-enabled/{site_name}'])

    subprocess.run(['nginx', '-t'])
    subprocess.run(['systemctl', 'reload', 'nginx'])

    

