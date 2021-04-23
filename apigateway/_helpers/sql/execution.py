import psycopg2


def execute_one(connection, command):
    try:
        cursor = connection.cursor()
        cursor.execute(command)
        cursor.close()
        connection.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def execute_many(connection, command, input_list):
    try:
        cursor = connection.cursor()
        cursor.executemany(command, input_list)
        cursor.close()
        connection.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def execute_query(connection, command, inputs: list):
    try:
        cursor = connection.cursor()
        cursor.execute(command, inputs)
        query = cursor.fetchall()
        cursor.close()
        connection.commit()
        return query
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return None
