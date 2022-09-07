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

