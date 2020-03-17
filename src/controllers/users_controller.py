from peewee import *
from user import User
import logging as log

db = SqliteDatabase("db/app.db")

class UsersController:
    '''
    Verify authentification
    '''

    def __init__(self, conn_page):
        self.page = conn_page

    def check_credentials(self):
        db.connect()

        # We get the user input : login and password
        login = self.page.login_entry.get()
        password = self.page.password_entry.get()

        # We search in the database the user with the corresponding login
        u = User.select().where(User.login == login).first()

        # We check if the login is right and then the password
        if u == None:
            self.page.display_notification("Authentification failed : no user found", "Red.TLabel")
        else:
            if password == u.password:
                log.info("Authentification successfull")
                self.controller.show_frame("EventsPage")
            else:
                self.page.display_notification("Authentification failed : password incorrect")

        db.close()

