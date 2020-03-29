from peewee import Model, SqliteDatabase, CharField, DateTimeField, ForeignKeyField
from models.user import User

db = SqliteDatabase("db/app.db")

class Vacation(Model):

    user = ForeignKeyField(User, backref='vacations')
    begin = DateTimeField()
    end = DateTimeField()
    reason = CharField()

    class Meta:
        database = db
        table_name = "vacations"


