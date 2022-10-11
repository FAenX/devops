from git.react_post_receive import create_react_post_receive
from database.database_queries import Database
import pymssql


def deploy_react_app(project_name):
    local_git_repo = create_react_post_receive(project_name)
    database = Database(connector='sqlserver')
    stored_procedure = 'sp_insert_project'

    results = database.execute_store_procedure(stored_procedure, (project_name, local_git_repo,  pymssql.output(str)))
    print(results)


    return results




    