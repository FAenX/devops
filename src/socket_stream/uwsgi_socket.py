import subprocess

# check if  /etc/systemd/system/devops.service  exists
# if not create it
def setup_uwsgi_socket(site_name, root_dir):
    "create and start uwsgi socket"
    config = f'''
    [Unit]
    Description=uWSGI instance to serve {root_dir}
    After=network.target
    
    [Service]
    User=www-data
    Group=www-data
    WorkingDirectory={root_dir}
    Environment="PATH={root_dir}/.venv/bin"
    ExecStart={root_dir}/.venv/bin/uwsgi --ini {root_dir}/uwsgi.ini
    
    [Install]
    WantedBy=multi-user.target'''
    
    with open(f'/etc/systemd/system/{site_name}.service', 'w') as f:
        f.write(config)
    
    subprocess.run(['systemctl', 'start', f'{site_name}.service'])
    subprocess.run(['systemctl', 'enable', f'{site_name}.service'])
    
    subprocess.run(['systemctl', 'status', f'{site_name}.service'])