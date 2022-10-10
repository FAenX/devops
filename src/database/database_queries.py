from .postgres_connection import Connection


def insert_into_database(
    table: str, 
    columns: list, 
    values: list
    ):
    connection = Connection()
    query = f"INSERT INTO {table}({', '.join(columns)}) VALUES ({', '.join(values)}) RETURNING *;"
   

    print(query)
    connection.execute(query)
    results = connection.fetchall()
    connection.close()

    print(results)

    return results
