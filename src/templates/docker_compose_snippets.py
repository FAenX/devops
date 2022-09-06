#!/usr/bin/env python3
import subprocess
import os
import yaml

class Wordpress:
    def __init__(self, project_name, db_name, db_user, db_password, port):
        self.name = project_name
        self.image = 'wordpress:latest'
        self.restart = 'always'
        self.ports = [f'{port}:80']
        self.volumes = [f'./{project_name}:/var/www/html']
        self.environment = {
            'WORDPRESS_DB_HOST': f'mysql_{project_name}',
            'WORDPRESS_DB_USER': db_user,
            'WORDPRESS_DB_PASSWORD': db_password,
            'WORDPRESS_DB_NAME': db_name
        }


    def __str__(self):
        return f'Name: {self.name}, Ports: {self.ports}, Volumes: {self.volumes}, Environment: {self.environment}'


class Mysql:
    def __init__(self, root_password, db_name, db_user, db_password, project_name):
        self.name = f'mysql_{project_name}'
        self.image = 'mysql:latest'
        self.restart = 'always'
        self.environment = {
            'MYSQL_ROOT_PASSWORD': root_password,
            'MYSQL_DATABASE': db_name,
            'MYSQL_USER': db_user,
            'MYSQL_PASSWORD': db_password
        }
        
        self.volumes = [f'./mysql_{project_name}:/var/lib/mysql']

    def __dict__(self):
        return {
            'name': self.name,
            'image': self.image,
            'restart': self.restart,
            'environment': self.environment,
            'volumes': self.volumes
        }

  

    def __str__(self):
        return f'Name: {self.name}, Image: {self.image}, Restart: {self.restart}, Environment: {self.environment}, Volumes: {self.volumes}'

class PhpMyAdmin:
    def __init__(self, my_admin_port, project_name):
        self.name = f'phpmyadmin_{project_name}'
        self.image = 'phpmyadmin/phpmyadmin'
        self.restart = 'always'
        self.volumes = [f'./{project_name}:/sessions']
        self.ports = [f'{my_admin_port}:80']
        self.environment = {
            'PMA_HOST': f'mysql_{project_name}',
            # 'PMA_ARBITRARY': '1'
        }


    def __str__(self):
        return f'Name: {self.name}, Image: {self.image}, Restart: {self.restart}, Ports: {self.ports}, Environment: {self.environment}'
   
class WordpressProject():
    def __init__(self, project_name, db_name, db_user, db_password, root_password, port, my_admin_port):
        self.wordpress = Wordpress(project_name, db_name, db_user, db_password, port)
        self.mysql = Mysql(root_password, db_name, db_user, db_password, project_name=project_name)
        self.phpmyadmin = PhpMyAdmin(my_admin_port, project_name=project_name) 
       
        
    def __str__(self):
        return f'Wordpress: {self.wordpress.__str__()}, Mysql: {self.mysql.__str__()}, PhpMyAdmin: {self.phpmyadmin.__str__()}'
    
    def __dict__(self):
        return {
            "version": "3.7",
            "services": {
                self.wordpress.name: {
                    "image": self.wordpress.image,
                    "restart": self.wordpress.restart,
                    "ports": self.wordpress.ports,
                    "volumes": self.wordpress.volumes,
                    "environment": self.wordpress.environment

                },
                self.mysql.name: {
                    "image": self.mysql.image,
                    "restart": self.mysql.restart,
                    "environment": self.mysql.environment,
                    "volumes": self.mysql.volumes
                },
                self.phpmyadmin.name: {
                    "image": self.phpmyadmin.image,
                    "restart": self.phpmyadmin.restart,
                    "ports": self.phpmyadmin.ports,
                    "environment": self.phpmyadmin.environment,
                    "volumes": self.phpmyadmin.volumes
                }


            }
        }
    
    def create_docker_compose_file(self):        
        with open(f'{os.path.expanduser("~/.devops")}/{self.wordpress.name}.yml', 'w') as file:
            documents = yaml.dump(self.__dict__(), file)
            print(documents)
            
    def start(self):
        self.create_docker_compose_file()
        
        try:
            subprocess.check_call(f'docker-compose -f ~/.devops/{self.wordpress.name}.yml up -d', shell=True)
            print('Wordpress is running')
        except Exception as e:
            print(e)
            raise e




   


