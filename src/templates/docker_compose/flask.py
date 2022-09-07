import subprocess
import yaml
from utils.config_object import config_object



class FlaskProject:
    def __init__(self, project_name, port):
        self.name = project_name
        self.image = 'python:3.7'
        self.restart = 'always'
        self.ports = [f'{port}:5000']
        self.volumes = [f'./{project_name}:/app']
        self.command = 'python app.py'
        self.environment = {
            'FLASK_APP': 'app.py'
        }
        


    def __str__(self):
        return f'Name: {self.name}, Ports: {self.ports}, Volumes: {self.volumes}, Environment: {self.environment}'

    def __dict__(self):
        return {
            "version": "3.7",
            "services": {
                self.name: {
                    "image": self.image,
                    "restart": self.restart,
                    "ports": self.ports,
                    "volumes": self.volumes,
                    "command": self.command,
                    "environment": self.environment
                }
            }
        }
        


    def write_docker_compose_file(self):
        config = config_object()

        # create project folder
        subprocess.check_call(f"mkdir -p {config['projects']}/{self.name}", shell=True)
        
        # create docker-compose.yml file
        path = f"{config['projects']}/{self.name}/docker-compose.yml"
        with open(path, 'w') as file:
            documents = yaml.dump(self.__dict__(), file)
            print(documents)
