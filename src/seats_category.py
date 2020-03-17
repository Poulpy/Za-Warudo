from peewee import Model, SqliteDatabase, CharField, DateTimeField, IntegerField, ForeignKeyField, Check
from category import Category
from projection_room import ProjectionRoom

db = SqliteDatabase("db/app.db")

class SeatsCategory(Model):

    projection_room = ForeignKeyField(ProjectionRoom, backref="seats_categories")
    category = ForeignKeyField(Category)
    seats = IntegerField(default = 0, constraints=[Check('seats >= 0')])

    class Meta:
        database = db
        table_name = "seats_categories"


