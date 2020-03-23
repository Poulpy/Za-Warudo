from peewee import Model, SqliteDatabase, CharField, DateTimeField, IntegerField, ForeignKeyField, Check

from models.category import Category
from models.event import Event
from models.projection_room import ProjectionRoom

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


