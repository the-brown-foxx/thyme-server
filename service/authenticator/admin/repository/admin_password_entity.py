from peewee import Model, TextField, IntegerField

from database.postgres import postgres_db


class AdminPasswordEntity(Model):
    hash: str = TextField()
    salt: str = TextField()
    version: int = IntegerField()

    class Meta:
        database = postgres_db
        db_table = 'admin_password'
