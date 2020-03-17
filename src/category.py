from peewee import Model, SqliteDatabase, CharField, DateTimeField, IntegerField, ForeignKeyField

db = SqliteDatabase("db/app.db")

class Category(Model):

    title = CharField()
    price = IntegerField(default=0)

    class Meta:
        database = db
        table_name = "categories"

