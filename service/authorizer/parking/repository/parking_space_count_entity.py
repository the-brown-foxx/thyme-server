from peewee import Model, IntegerField

from database.postgres import postgres_db

class ParkingSpaceCountEntity(Model):
    total_space = IntegerField()
    vacant_space = IntegerField()

    class Meta:
        database = postgres_db
        db_table = 'parking_space_count'
