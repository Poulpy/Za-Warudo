# from peewee import SqliteDatabase, Model, CharField
from peewee import *

db = SqliteDatabase("db/app.db")

class Debate(Model):
    speaker = CharField()
    contact_details = CharField()

    class Meta:
        database = db
        table_name = "debates"

