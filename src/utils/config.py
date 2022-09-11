import os
import yaml


class DevopsConfig:
    def __init__(self, production=False, digital_ocean_token=None):
        self.config_file_name = "config.yml"
        self.devops_home = os.path.expanduser("~/.devops")
        self.git = f"{self.devops_home}/git"
        self.www = f"{self.devops_home}/www"
        self.tmp = f"{self.devops_home}/tmp"
        self.projects = f"{self.devops_home}/projects"
        self.devops_config_file = f"{self.devops_home}/{self.config_file_name}"
        self.minikube_dir = f"{self.devops_home}/minikube"
        self.docker_registry = "localhost:5000"
        self.production = production
        self.digital_ocean_token = digital_ocean_token

    def __str__(self):
        return f"Devops config folder: {self.devops_home}"

    def create_directories_if_not_exists(self):
        os.makedirs(self.devops_home, exist_ok=True)
        os.makedirs(self.git, exist_ok=True)
        os.makedirs(self.tmp, exist_ok=True)
        os.makedirs(self.projects, exist_ok=True)
        os.makedirs(self.minikube_dir, exist_ok=True)

    def create_config_file_if_not_exists(self):
        if not os.path.exists(self.devops_config_file):
            with open(self.devops_config_file, 'w') as file:
                documents = yaml.dump(self.__dict__(), file)
                print(documents)

    def read_config_file(self):
        self.create_config_file_if_not_exists()
        with open(self.devops_config_file, 'r') as file:
            return yaml.load(file, Loader=yaml.FullLoader)

    def update_config_file(self, key, value):
        config = self.read_config_file()
        config[key] = value
        with open(self.devops_config_file, 'w') as file:
            documents = yaml.dump(config, file)
            print(documents)

    def __dict__(self):
        return {
            "git": self.git,
            "www": self.www,
            "tmp": self.tmp,
            "devops_config_file": self.devops_config_file,
            "devops_home": self.devops_home,
            "config_file_name": self.config_file_name,
            "projects": self.projects,
            "minikube_dir": self.minikube_dir,
            "docker_registry": self.docker_registry,
            "production": self.production,
            "digital_ocean_token": self.digital_ocean_token
            
        }