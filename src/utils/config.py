import os
import yaml


class DevopsConfig:
    def __init__(self):
        self.config_file_name = "config.yml"
        self.devops_home = os.path.expanduser("~/.devops")
        self.git = f"{self.devops_home}/git"
        self.www = f"{self.devops_home}/www"
        self.tmp = f"{self.devops_home}/tmp"
        self.projects = f"{self.devops_home}/projects"
        self.devops_config_file = f"{self.devops_home}/{self.config_file_name}"

    def __str__(self):
        return f"Devops config folder: {self.devops_home}"

    def create_directories(self):
        os.makedirs(self.devops_home, exist_ok=True)
        os.makedirs(self.git, exist_ok=True)
        os.makedirs(self.tmp, exist_ok=True)
        os.makedirs(self.projects, exist_ok=True)

    def create_config_file_if_not_exists(self):
        if not os.path.exists(self.devops_config_file):
            with open(self.devops_config_file, 'w') as file:
                documents = yaml.dump(self.__dict__(), file)
                print(documents)

    def read_config_file(self):
        with open(self.devops_config_file, 'r') as file:
            return yaml.load(file, Loader=yaml.FullLoader)

    def __dict__(self):
        return {
            "git": self.git,
            "www": self.www,
            "tmp": self.tmp,
            "devops_config_file": self.devops_config_file,
            "devops_home": self.devops_home,
            "config_file_name": self.config_file_name,
            "projects": self.projects
        }