from typing import Optional

from peewee import *
from os import getenv

POSTGRES_PASSWORD = getenv('POSTGRES_PASSWORD')

postgres_db = PostgresqlDatabase(
    database='postgres',
    user='postgres',
    password=POSTGRES_PASSWORD,
    host='localhost',
    port=5469,
)


class CarEntity(Model):
    registration_id: str = TextField()
    make: str = TextField()
    model: str = TextField()
    year: int = IntegerField()
    owner: str = TextField()
    temporary_password: Optional[str] = TextField(null=True)
    password_hash: Optional[str] = TextField(null=True)
    password_salt: Optional[str] = TextField(null=True)

    class Meta:
        database = postgres_db
        db_table = 'car'
