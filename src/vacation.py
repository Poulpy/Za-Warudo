from peewee import Model, SqliteDatabase, CharField, DateTimeField, IntegerField, ForeignKeyField
from user import User

db = SqliteDatabase("db/app.db")

class Vacation(Model):

    user = ForeignKeyField(User)
    begin = DateTimeField()
    end = DateTimeField()
    reason = CharField()

    class Meta:
        database = db
        table_name = "vacations"


