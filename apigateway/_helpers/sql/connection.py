import psycopg2
from decouple import config
from psycopg2 import Error


def establish_connection():
    try:
        connection = psycopg2.connect(user=config('DB_USER', default='postgres'),
                                      password=config('DB_PASSWORD', default='postgres'),
                                      host=config('DB_HOST', default='127.0.0.1'),
                                      port=config('DB_PORT', default=5432),
                                      database=config('DB_NAME', default='postgres')
                                      )
        return connection
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)


def close_connection(connection):
    connection.close()
