from peewee import Model, CharField, BooleanField, SqliteDatabase

db = SqliteDatabase("db/app.db")

class User(Model):
    name = CharField()
    login = CharField()
    password = CharField()
    is_admin = BooleanField(default=False)

    def __str__(self):
        return "[User] name: " + self.name + ", login: " + self.login

    class Meta:
        database = db
        table_name = "users"

