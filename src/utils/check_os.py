import os
import csv

def check_os():
    if os.path.isfile('/etc/os-release'):
        with open('/etc/os-release') as f:
            reader = csv.reader(f, delimiter="=")
            os_release = dict(reader)
            if os_release['ID'] == 'ubuntu':
                return 'ubuntu'
            elif os_release.get('ID_LIKE') == 'debian':
                return 'debian'
            else :
                return 'unknown'
    else:
        return 'unknown'