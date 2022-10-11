import pymssql
import os
import sys

class SqlServerConnection:
    def __init__(self, server, database, username, password):
        self.server = server
        self.database = database
        self.username = username
        self.password = password           
        self.connection = pymssql.connect(self.server, self.username, self.password, self.database)
        self.cursor = self.connection.cursor(as_dict=True)

    def execute(self, query):
        self.cursor.execute(query)
        self.connection.commit()

    # store procedure
    def execute_store_procedure(self, store_procedure_name, data):
        s = self.cursor.callproc(store_procedure_name, data)
        print(s[-1])
        self.connection.commit()
        return s[-1]


    def execute_many(self, query, data):
        self.cursor.executemany(query, data)
        self.connection.commit()

    def fetch(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def close(self):
        self.connection.close()