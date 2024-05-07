from typing import Optional

from peewee import Model, TextField, IntegerField

from database.postgres import postgres_db


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
