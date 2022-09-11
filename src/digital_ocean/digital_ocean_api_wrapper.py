import subprocess

def list_droplets():
    try:
        subprocess.check_call('''
        curl -X GET \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer $DIGITALOCEAN_TOKEN" \
        "https://api.digitalocean.com/v2/droplets/"
        '''
        , shell=True)
    except:
        print('doctl not installed')