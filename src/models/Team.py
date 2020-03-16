from peewee import SqliteDatabase, Model, ForeignKeyField
from models import User, Event

db = SqliteDatabase("db/app.db")

class Team(Model):
    member = ForeignKeyField(User)
    event = ForeignKeyField(Event)

    def __str__(self):
        return "[User] name: " + self.name + ", login: " + self.login

    class Meta:
        database = db
        table_name = "teams"

