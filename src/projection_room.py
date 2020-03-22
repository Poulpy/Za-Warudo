from peewee import SqliteDatabase, Model, CharField, IntegerField, Check

db = SqliteDatabase("db/app.db")

class ProjectionRoom(Model):
    '''
    The place where the film is being screened
    '''

    location = CharField()
    total_seats = IntegerField(default=0, constraints=[Check('total_seats >= 0')])

    class Meta:
        database = db
        table_name = "projection_rooms"


