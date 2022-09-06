
from templates.docker_compose_snippets import WordpressProject

def setup_wordpress_in_docker():
    project_name = input('Enter project name: ')
    db_name = input('Enter database name: ')
    db_user = input('Enter database user: ')
    db_password = input('Enter database password: ')
    root_password = input('Enter root password: ')
    port = input('Enter port: ')
    my_admin_port = input('Enter phpmyadmin port: ')

    wp_project = WordpressProject(
        project_name=project_name,
        db_name=db_name, 
        db_user=db_user,
        db_password=db_password,
        root_password=root_password,
        port=port,
        my_admin_port=my_admin_port
        )

    wp_project.create_docker_compose_file()
    wp_project.start()