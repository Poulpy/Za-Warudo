from peewee import Model, SqliteDatabase, CharField, DateTimeField, IntegerField, ForeignKeyField, Check

db = SqliteDatabase("db/app.db")

class Category(Model):
    '''
    Categories of fees: teenagers, elderly, disabled
    '''

    title = CharField()
    price = IntegerField(default=0, constraints=[Check('price >= 0')])

    class Meta:
        database = db
        table_name = "categories"

