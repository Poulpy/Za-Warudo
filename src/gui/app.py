from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedStyle
from gui.connection_page import ConnectionPage
from gui.events_page import EventsPage
from peewee import *
from user import User
from event import Event
import logging as log
from datetime import datetime

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

        self.geometry("400x600")
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
        self.set_menu(False)


    def set_menu(self, is_connected: bool):
        menubar = Menu(self)
        pmenu = Menu(menubar, tearoff=0)
        if is_connected:
            pmenu.add_command(label="Timetable")
            pmenu.add_command(label="New vacation")
            pmenu.add_command(label="Log out", command=lambda: self.show_frame("ConnectionPage"))
        pmenu.add_command(label="Exit", command=self.destroy)
        menubar.add_cascade(label="Fichier", menu=pmenu)
        self.config(menu=menubar)

    def get_events(self, date_str: str):
        db.connect()
        log.info(date_str)
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
        events = Event.select().where((Event.begin.year == date.year)
                                    & (Event.begin.month == date.month)
                                    & (Event.begin.day == date.day))
        db.close()
        for event in events.dicts():
            log.info(event)
        return events

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

        if page_name == "ConnectionPage":
            self.set_menu(False)
        else:
            self.set_menu(True)

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

