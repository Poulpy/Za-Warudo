import unittest
from peewee import *
from models.User import User

db = SqliteDatabase("db/test.db")

class TestDataBase(unittest.TestCase):

    def test_connection(self):
        db.connect()
        db.create_tables([User])
        # tmp = User.create(name="Test", login="changeme", password="changeme")
        print("Users count : " + str(User.select().count()))
        for user in User.select():
            print(user)

        # tmp.delete_instance()

        db.close()

    def test_login(self):
        db.connect()
        db.create_tables([User])
        u = User.select().where(User.login=="jgaspar").first()
        self.assertEqual(u.password, "changeme")

        db.close()

if  __name__ == '__main__':
    unittest.main()

