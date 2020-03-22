from peewee import Model, SqliteDatabase, CharField, DateTimeField, IntegerField, ForeignKeyField, Check
from category import Category
from event import Event
from projection_room import ProjectionRoom

db = SqliteDatabase("db/app.db")

class EventsCategory(Model):
    '''
    An event can have multiple fees, and a fee can belong to many events
    '''

    event = ForeignKeyField(Event)
    category = ForeignKeyField(Category)

    class Meta:
        database = db
        table_name = "events_categories"


