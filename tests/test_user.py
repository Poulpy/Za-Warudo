import unittest

from peewee import *

from models.user import User

db = SqliteDatabase("db/test.db")

class TestUser(unittest.TestCase):

    def test_connection(self):
        db.connect()
        db.create_tables([User])
        print("Users count : " + str(User.select().count()))
        for user in User.select():
            print(user)


        db.close()

    def test_login(self):
        db.connect()
        db.create_tables([User])
        u = User.select().where(User.login=="jgaspar").first()
        self.assertEqual(u.password, "changeme")

        db.close()

    def test_none(self):
        db.connect()
        db.create_tables([User])
        u = User.select().where(User.login=="zefioezhoeihaer").first()
        self.assertEqual(u, None)

        db.close()

if  __name__ == '__main__':
    unittest.main()

