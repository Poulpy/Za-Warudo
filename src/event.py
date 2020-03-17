# from peewee import Model, SqliteDatabase, CharField, DateTimeField, IntegerField, ForeignKeyField
from user import User
from projection_room import ProjectionRoom
from debate import Debate
from peewee import *

db = SqliteDatabase("db/app.db")

class Event(Model):
    status = CharField(default="created")# in progress, finished

    name = CharField()
    begin = DateTimeField()
    end = DateTimeField()

    sold_seats = IntegerField(default=0)
    booked_seats = IntegerField(default=0)
    revenue = IntegerField(default = 0)

    room_reserved = BooleanField(default = False)
    equipment_reserved = BooleanField(default = False)
    management = BooleanField(default = False)
    guest_attendance = BooleanField(default = False)

    responsible = ForeignKeyField(User, backref="events")
    projection_room = ForeignKeyField(ProjectionRoom, backref="events")
    debate = ForeignKeyField(Debate, backref="events")

    class Meta:
        database = db
        table_name = "events"

