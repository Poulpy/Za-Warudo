from datetime import datetime
from tkinter import *
from tkinter import ttk
import logging as log

from peewee import *
from ttkthemes import ThemedStyle

from models.event import Event
from gui.connection_page import ConnectionPage
from gui.edit_event_page import EditEventPage
from gui.events_page import EventsPage
from models.projection_room import ProjectionRoom
from models.user import User
from models.team import Team
from models.category import Category
from models.events_category import EventsCategory

db = SqliteDatabase("db/app.db")

class App(Tk):
    '''
    The controller of the application
    Stores all events handler
    '''

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        container = ttk.Frame(self)
        # We use the 'breeze' theme because it's the most beautiful
        # theme along with 'arc'
        style = ThemedStyle(self)
        style.set_theme("breeze")

        self.geometry("1200x550")
        self.minsize(300, 300)
        self.title("Za Warudo")

        # We want the current user logged in to be available from
        # everywhere, like in rails
        self.user = None

        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Styles
        s = ttk.Style()
        s.configure("Red.TLabel", foreground="red")
        s.configure("Treeview", rowheight=30)

        # All frames of the application
        # TODO make it dynamic
        self.frames = {}

        for P in (ConnectionPage, EventsPage, EditEventPage):
            page_name = P.__name__
            frame = P(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
            # frame.grid_propagate(0)

        self.show_frame("ConnectionPage")
        self.set_menu(is_connected=False)


    def set_menu(self, is_connected: bool):
        '''
        Show a menu on top of the window
        '''

        menubar = Menu(self)

        # 2 menus
        pmenu = Menu(menubar, tearoff=0)
        help_menu = Menu(menubar, tearoff=0)

        if is_connected:
            pmenu.add_command(label="Timetable")
            pmenu.add_command(label="New vacation")
            pmenu.add_command(label="Log out", command=lambda: self.show_frame("ConnectionPage"))
            pmenu.add_separator()

        pmenu.add_command(label="Exit", command=self.destroy)
        help_menu.add_command(label="About")

        # We add all the menus
        menubar.add_cascade(label="Za Warudo", menu=pmenu)
        menubar.add_cascade(label="Help", menu=help_menu)

        self.config(menu=menubar)

    def get_events(self, date_str: str):
        '''
        Return all events from the database, according to the date
        given in argument (format : "%Y-%m-%d")
        TODO pass the format in argument for flexibility
        '''

        db.connect()

        log.info(date_str)

        date = datetime.strptime(date_str, "%Y-%m-%d").date()
        events = Event.select().where((Event.begin.year == date.year)
                                    & (Event.begin.month == date.month)
                                    & (Event.begin.day == date.day))

        db.close()

        return events

    def get_categories(self):
        '''
        Return all categories
        '''
        db.connect()
        categories = Category.select()
        db.close()

        return categories


    def get_projection_rooms(self):
        '''
        Return all projection rooms
        '''

        db.connect()
        proj_rooms = ProjectionRoom.select()
        db.close()

        return proj_rooms

    def get_users(self):
        '''
        Return all users
        '''

        db.connect()
        users = User.select()
        db.close()

        return users

    def update_events_page(self):
        '''
        Update the events displayed in the events page
        '''

        self.frames["EventsPage"].set_displayed_events()

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''

        frame = self.frames[page_name]
        frame.tkraise()

        # There are some menu items/options that are only visible
        # to logged in users
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
                self.current_user = u
                log.info("Authentification successfull")
                self.show_frame("EventsPage")
            else:
                self.frames["ConnectionPage"].display_notification("Authentification failed : password incorrect", "Red.TLabel")

        db.close()

    def create_event(self, event):
        '''
        Create a event with a dict given in argument
        '''
        event['projection_room'] = ProjectionRoom.get(ProjectionRoom.location == event['projection_room']).id
        event['begin'] = datetime.strptime(event['begin'], "%Y-%m-%d %H:%M")
        event['responsible'] = self.current_user.id
        event_created = Event.create(**event)

        return event_created.id

    def create_team(self, member_names, event_id):
        team = [{'member':User.get(User.name == name).id, 'event':event_id} for name in member_names]
        print(team)
        Team.insert_many(team).execute()

    def create_events_categories(self, cat_titles, event_id):
        cats = [{'category':Category.get(Category.title == title).id, 'event':event_id} for title in cat_titles]
        print(cats)
        EventsCategory.insert_many(cats).execute()



