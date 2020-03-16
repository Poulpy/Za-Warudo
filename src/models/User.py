from peewee import *

db = SqliteDatabase("app.db")

class User(Model):
    name = CharField()
    login = CharField()
    password = CharField()

    class Meta:
        database = db
        table_name = "users"

