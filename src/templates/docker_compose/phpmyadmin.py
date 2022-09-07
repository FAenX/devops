class PhpMyAdmin:
    def __init__(self, my_admin_port, project_name):
        self.name = f'phpmyadmin_{project_name}'
        self.image = 'phpmyadmin/phpmyadmin'
        self.restart = 'always'
        self.volumes = [f'./phpmyadmin_{project_name}:/sessions']
        self.ports = [f'{my_admin_port}:80']
        self.environment = {
            'PMA_HOST': f'mysql_{project_name}',
            # 'PMA_ARBITRARY': '1'
        }


    def __str__(self):
        return f'Name: {self.name}, Image: {self.image}, Restart: {self.restart}, Ports: {self.ports}, Environment: {self.environment}'