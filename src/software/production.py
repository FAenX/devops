import subprocess
# install nginx if user is root and os is ubuntu or debian
def install_nginx_if_not_exists():
    # if nginx already installed do nothing
    try:
        subprocess.run(['nginx', '-v'])
        return
    except:        
        subprocess.run(['apt-get', 'update'])
        subprocess.run(['apt-get', 'install', 'nginx', '-y'])
        subprocess.run(['systemctl', 'enable', 'nginx'])
        subprocess.run(['systemctl', 'start', 'nginx'])




# install all software
def install_all():
    install_nginx_if_not_exists()