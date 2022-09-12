import subprocess
import os
import yaml
import inquirer
import csv


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
        self.create_directories_if_not_exists()
        self.create_config_file_if_not_exists()
        self.digital_ocean_token = digital_ocean_token
        self.config = self.read_config_file()
        self.set_digital_ocean_token()
        self.install_minikube_if_not_exists()

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

    def set_digital_ocean_token(self):
        print(self.config)
        if not self.config.get('digital_ocean_token'):
            questions = [
                inquirer.Text('token', message="Enter your Digital Ocean token")
            ]
            answers = inquirer.prompt(questions)
            self.config['digital_ocean_token'] = answers['token']
            self.update_config_file('digital_ocean_token', answers['token'])

    # check os distro
    def check_os(self):
        if os.path.isfile('/etc/os-release'):
            with open('/etc/os-release') as f:
                reader = csv.reader(f, delimiter="=")
                os_release = dict(reader)
                if os_release['ID'] == 'ubuntu':
                    return 'ubuntu'
                elif os_release['ID'] == 'debian':
                    return 'debian'
                elif os_release.get('ID_LIKE') == 'debian':
                    return 'debian'
                else :
                    return 'unknown'
        else:
            return 'unknown'
            # 

    



    def install_minikube_if_not_exists(self):     

        os_check = self.check_os()
        if os_check == 'unknown':
            raise Exception('Unknown OS')


        # if not production use docker else install qemu
        if self.production:
            # install_qemu()
            pass
        else:
            try:
                subprocess.check_call('docker -v', shell=True)
            
            except:
                subprocess.check_call('apt-get install docker.io -y', shell=True) 
                # enablea nd start docker
                subprocess.check_call('systemctl enable docker', shell=True)


        try:
            subprocess.check_call(f'minikube -h > /dev/null 2>&1', shell=True)
        except Exception as e:     
            # print(e)  
            print('executing minikube install')
            subprocess.check_call(f'curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64 && chmod +x minikube-linux-amd64 && mv minikube-linux-amd64 {self.minikube_dir}/minikube && {self.minikube_dir}/minikube start --force', shell=True, cwd=self.minikube_dir)
            # add minikube path to bashrc
            subprocess.check_call(f'echo "export PATH=$PATH:{self.minikube_dir}" >> ~/.bashrc', shell=True)
            # source bashrc
            # subprocess.check_call(f'source ~/.bashrc', shell=True)
            # 
        try:
            subprocess.check_call(f'kubectl version --client', shell=True)
        except:
            subprocess.check_call(f'curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl && chmod +x kubectl && mv kubectl {self.minikube_dir}/', shell=True)
            # add kubectl to path
            subprocess.check_call(f'export PATH={self.minikube_dir}:$PATH', shell=True)
        try:
            subprocess.check_call('docker-compose -v', shell=True)
        except:
            subprocess.check_call('apt-get install docker-compose -y', shell=True)


        # add minikube to path if not already there
        if not os.environ['PATH'].find(self.minikube_dir) > -1:
            os.environ['PATH'] = os.environ['PATH'] + ':' + self.minikube_dir
        

    
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
            "production": self.production
            
        }