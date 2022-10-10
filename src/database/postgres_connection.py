import psycopg2


class Connection:
    def __init__(self):
        self.connection = psycopg2.connect(
            host="localhost",
            database="rusha",
            user="postgres",
            password="postgres"
        )
        self.cursor = self.connection.cursor()

    def execute(self, query):
        self.cursor.execute(query)
        self.connection.commit()

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def close(self):
        self.cursor.close()
        self.connection.close()