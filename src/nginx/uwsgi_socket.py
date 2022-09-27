import subprocess

# check if  /etc/systemd/system/devops.service  exists
# if not create it
def setup_uwsgi_socket(SOCKET, ROOT_DIR):
    "create and start uwsgi socket"
    config = f'''
    [Unit]
    Description=uWSGI instance to serve {ROOT_DIR}
    After=network.target
    
    [Service]
    User=www-data
    Group=www-data
    WorkingDirectory={ROOT_DIR}
    Environment="PATH={ROOT_DIR}/.venv/bin"
    ExecStart={ROOT_DIR}/.venv/bin/uwsgi --ini {ROOT_DIR}/uwsgi.ini
    
    [Install]
    WantedBy=multi-user.target'''
    
    with open(f'/etc/systemd/system/{SOCKET}.service', 'w') as f:
        f.write(config)
    
    subprocess.run(['systemctl', 'start', f'{SOCKET}.service'])
    subprocess.run(['systemctl', 'enable', f'{SOCKET}.service'])
    
    subprocess.run(['systemctl', 'status', f'{SOCKET}.service'])