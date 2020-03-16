import unittest
from peewee import *
from models.User import User

db = SqliteDatabase("app.db")

class TestDataBase(unittest.TestCase):

    def test_connection(self):
        db.connect()
        db.create_tables([User])
        User.create(name="Paul", login="changeme", password="changeme")
        for user in User.select():
            print("User : " + user.name)

if  __name__ == '__main__':
    unittest.main()

