from .postgres_connection import Connection
from .sqlserver_connection import SqlServerConnection

class Database:
    def __init__(self, connector: str = 'sqlserver'):
        self.connector = connector

    def execute_query( self,  query: str):
        if self.connector == 'sqlserver':
            connection = SqlServerConnection(
                server='localhost',
                database='rusha',
                username='sa',
                password='Your_password123'
            )
            connection.execute(query)
            results = connection.fetch(query)
            connection.close()
            return results

        elif self.connector == 'postgres':
            pass

    # store procedure
    def execute_store_procedure(self, store_procedure_name: str, data: tuple):
        if self.connector == 'sqlserver':
            connection = SqlServerConnection(
                server='localhost',
                database='rusha',
                username='sa',
                password='Your_password123'
            )
            result = connection.execute_store_procedure(store_procedure_name, data)
            print(result)
            connection.close()
            return result

        elif self.connector == 'postgres':
            pass

            

    
