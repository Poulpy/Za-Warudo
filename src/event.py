# from peewee import Model, SqliteDatabase, CharField, DateTimeField, IntegerField, ForeignKeyField
from user import User
from projection_room import ProjectionRoom
from debate import Debate
from peewee import *
import datetime

db = SqliteDatabase("db/app.db")

class Event(Model):
    status = CharField(default="created")# in progress, finished

    name = CharField()
    begin = DateTimeField(default=datetime.datetime.now())
    end = DateTimeField(default=datetime.datetime.now() + datetime.timedelta(hours=2))

    sold_seats = IntegerField(default=0, constraints=[Check('sold_seats >= 0')])
    booked_seats = IntegerField(default=0, constraints=[Check('booked_seats >= 0')])
    revenue = IntegerField(default = 0, constraints=[Check('revenue >= 0')])

    room_reserved = BooleanField(default = False)
    equipment_reserved = BooleanField(default = False)
    management = BooleanField(default = False)
    guest_attendance = BooleanField(default = False)

    responsible = ForeignKeyField(User, backref="events")
    projection_room = ForeignKeyField(ProjectionRoom, backref="events", null = False)
    debate = ForeignKeyField(Debate, backref="events", null = True)

    class Meta:
        database = db
        table_name = "events"

