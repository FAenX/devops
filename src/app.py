from flask import Flask
server = Flask(__name__)
from src.run_files.applications import minikube_flask

@server.route("/")
def hello():
    minikube_flask('project_d')
    return "Hello World!"

if __name__ == "__main__":
   server.run(host='0.0.0.0')