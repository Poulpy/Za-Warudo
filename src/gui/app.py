from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedStyle
from gui.connection_page import ConnectionPage
from gui.events_page import EventsPage
from peewee import *
from user import User
import logging as log

db = SqliteDatabase("db/app.db")

class App(Tk):
    '''
    The controller of the application
    Stores all events handler
    '''

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        # self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        container = ttk.Frame(self)
        style = ThemedStyle(self)
        style.set_theme("arc")

        self.geometry("600x600")
        self.minsize(300, 300)
        self.title("ZA WARUDO")

        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Styles
        s = ttk.Style()
        s.configure("Red.TLabel", foreground="red")

        self.frames = {}

        for P in (ConnectionPage, EventsPage):
            page_name = P.__name__
            frame = P(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)

        self.show_frame("ConnectionPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

    def check_credentials(self, event=None):
        '''
        Event raised when the user click on the login button
        on the connection page
        '''
        db.connect()

        # We get the user input : login and password
        login = self.frames["ConnectionPage"].login_entry.get()
        password = self.frames["ConnectionPage"].password_entry.get()

        # We search in the database the user with the corresponding login
        u = User.select().where(User.login == login).first()

        # We check if the login is right and then the password
        if u == None:
            self.frames["ConnectionPage"].display_notification("Authentification failed : no user found", "Red.TLabel")
        else:
            if password == u.password:
                self.frames["ConnectionPage"].display_notification("", "TLabel")
                log.info("Authentification successfull")
                self.show_frame("EventsPage")
            else:
                self.frames["ConnectionPage"].display_notification("Authentification failed : password incorrect", "Red.TLabel")

        db.close()

