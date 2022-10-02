import subprocess


def setup_nginx_to_localhost(site_name, server, proxy_pass):
    "create and nginx configuration"
    config = f'''
    server {{
        server_name {server};
        client_max_body_size 50M;
        access_log  /var/log/nginx/{site_name}.access.log;
        error_log   /var/log/nginx/{site_name}.error.log;
        location / {{
            proxy_pass {proxy_pass};
        }}
    }}'''

    with open(f'/etc/nginx/sites-available/{site_name}', 'w') as f:
        f.write(config)

    subprocess.run(['ln', '-s', f'/etc/nginx/sites-available/{site_name}', f'/etc/nginx/sites-enabled/{site_name}'])

    subprocess.run(['nginx', '-t'])
    subprocess.run(['systemctl', 'reload', 'nginx'])