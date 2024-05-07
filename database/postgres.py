from os import getenv

from peewee import PostgresqlDatabase

POSTGRES_PASSWORD = getenv('POSTGRES_PASSWORD')

postgres_db = PostgresqlDatabase(
    database='postgres',
    user='postgres',
    password=POSTGRES_PASSWORD,
    host='localhost',
    port=5469,
)
