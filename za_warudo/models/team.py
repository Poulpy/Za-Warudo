from peewee import SqliteDatabase, Model, ForeignKeyField

from models.user import User
from models.event import Event

db = SqliteDatabase("db/app.db")

class Team(Model):
    '''
    A user can participate in the organisation of an
    event : that's a member of a team
    '''

    member = ForeignKeyField(User, backref='teams')
    event = ForeignKeyField(Event, backref='teams')

    def __str__(self):
        return "[User] name: " + self.name + ", login: " + self.login

    class Meta:
        database = db
        table_name = "teams"

