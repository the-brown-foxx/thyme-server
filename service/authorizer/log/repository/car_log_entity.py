from datetime import datetime

from peewee import Model, TextField, DateTimeField, BooleanField, AutoField

from database.postgres import postgres_db


class CarLogEntity(Model):
    log_id = AutoField(primary_key=True)
    date_time = DateTimeField()
    car_registration_id = TextField()
    entering = BooleanField()
    image = TextField()
    sus = BooleanField()

    class Meta:
        database = postgres_db
        db_table = 'logs'
