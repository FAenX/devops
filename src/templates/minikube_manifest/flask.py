import yaml
from utils.config_object import config_object
import subprocess


class FlaskProjectMiniKube:
    def __init__(self, project_name):
        self.project_name = project_name

    def pod(self):
        return {
            "apiVersion": "v1",
            "kind": "Pod",
            "metadata": {
                "name": self.project_name
            },
            "spec": {
                "containers": [
                    {
                        "name": self.project_name,
                        "image": f"{self.project_name}:latest",
                        "ports": [
                            {
                                "containerPort": 5000
                            }
                        ]
                    }
                ]
            }
        }

    def deployment(self):
        return {
            "apiVersion": "apps/v1",
            "kind": "Deployment",
            "metadata": {
                "name": self.project_name
            },
            "spec": {
                "replicas": 1,
                "selector": {
                    "matchLabels": {
                        "app": self.project_name
                    }
                },
                "template": {
                    "metadata": {
                        "labels": {
                            "app": self.project_name
                        }
                    },
                    "spec": {
                        "containers": [
                            {
                                "name": self.project_name,
                                "image": f"{self.project_name}:latest",
                                "ports": [
                                    {
                                        "containerPort": 5000
                                    }
                                ]
                            }
                        ]
                    }
                }
            }
        }

    def service(self):
        return {
            "apiVersion": "v1",
            "kind": "Service",
            "metadata": {
                "name": f"{self.project_name.replace('_', '-')}-service"
            },
            "spec": {
                "type": "NodePort",
                "ports": [
                    {
                        "port": 5000,
                        "targetPort": 5000
                    }
                ],
                "selector": {
                    "app": self.project_name
                }
            }
        }

    def __str__(self):
        return f'Name: {self.name}, Image: {self.image}, Restart: {self.restart}, Ports: {self.ports}, Environment: {self.environment}'

    def create_manifest(self):
        config = config_object()
        path = f"{config['projects']}/{self.project_name}/{self.project_name}.yml"
        subprocess.check_call(f"mkdir -p {config['projects']}/{self.project_name}", shell=True)
        with open(path, 'w') as f:
            f.write(yaml.dump(self.pod()))
            f.write(yaml.dump(self.deployment()))
            f.write(yaml.dump(self.service()))