from peewee import Model, SqliteDatabase, CharField, DateTimeField, IntegerField, ForeignKeyField
from models import User, ProjectionRoom, Debate

db = SqliteDatabase("db/app.db")

class Event(Model):
    status = CharField(default="created")
    name = CharField()
    begin = DateTimeField()
    end = DateTimeField()
    sold_seats = IntegerField(default=0)
    booked_seats = IntegerField(default=0)
    responsible = ForeignKeyField(User, backref="events")
    projection_room = ForeignKeyField(ProjectionRoom, backref="events")
    debate = ForeignKeyField(Debate, backref="events")

    class Meta:
        database = db
        table_name = "events"

