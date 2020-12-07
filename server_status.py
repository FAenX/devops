import requests

def server_status(url):
    return requests.get(url)


if __name__=='__main__':
    response = server_status('https://boma-api.touchinspiration.net/login').status_code
    print(response)