from git.react_post_receive import create_react_post_receive
from database.database_queries import insert_into_database


def deploy_react_app(project_name):
    git_repo = create_react_post_receive(project_name)

    # insert into postgres database
    # insert into postgres database
    table = 'devops.projects'
    columns = ['project_name', 'internal_git_repo']
    values = [f'\'{project_name}\'', f'\'{git_repo}\'']
    results = insert_into_database(table, columns, values)



    return results


    