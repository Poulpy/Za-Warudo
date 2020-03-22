from peewee import SqliteDatabase, Model, ForeignKeyField
from user import User
from event import Event

db = SqliteDatabase("db/app.db")

class Team(Model):
    '''
    A user can participate in the organisation of an
    event : that's a member of a team
    '''

    member = ForeignKeyField(User)
    event = ForeignKeyField(Event)

    def __str__(self):
        return "[User] name: " + self.name + ", login: " + self.login

    class Meta:
        database = db
        table_name = "teams"

