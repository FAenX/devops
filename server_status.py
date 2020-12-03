import requests

def server_status(url):
    return requests.get(url)


if __name__=='__main__':
    response = server_status('https://google.com').status_code
    print(response)