import datetime

from peewee import Model, SqliteDatabase, CharField, DateTimeField, IntegerField, ForeignKeyField, BooleanField, Check

from models.projection_room import ProjectionRoom
from models.user import User

db = SqliteDatabase("db/app.db")

class Event(Model):
    status = CharField(default="created")# in progress, finished

    name = CharField()
    begin = DateTimeField(default=datetime.datetime.now())
    running_time = IntegerField(default=120, constraints=[Check('running_time >= 0')])
    projection_type = CharField()

    sold_seats = IntegerField(default=0, constraints=[Check('sold_seats >= 0')])
    booked_seats = IntegerField(default=0, constraints=[Check('booked_seats >= 0')])
    revenue = IntegerField(default = 0, constraints=[Check('revenue >= 0')])

    room_reserved = BooleanField(default = False)
    equipment_reserved = BooleanField(default = False)
    management = BooleanField(default = False)
    guest_attendance = BooleanField(default = False)
    debate = BooleanField(default = False)
    presentation = BooleanField(default = False)

    manager = ForeignKeyField(User, backref="events")
    projection_room = ForeignKeyField(ProjectionRoom, backref="events")

    class Meta:
        database = db
        table_name = "events"

