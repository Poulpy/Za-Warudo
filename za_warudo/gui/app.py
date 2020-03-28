from functools import partial
from datetime import datetime
from tkinter import *
from tkinter import ttk
import logging as log

from peewee import *
from ttkthemes import ThemedStyle

from gui.connection_page import ConnectionPage
from gui.edit_event_page import EditEventPage
from gui.events_page import EventsPage
from gui.show_event_page import ShowEventPage
from gui.ticketing_page import TicketingPage
from models.category import Category
from models.event import Event
from models.events_category import EventsCategory
from models.projection_room import ProjectionRoom
from models.team import Team
from models.user import User

db = SqliteDatabase("db/app.db")

class App(Tk):
    '''
    The controller of the application
    Stores all events handler
    '''

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        container = ttk.Frame(self)
        db.connect()
        self.protocol('WM_DELETE_WINDOW', self.app_will_quit)
        # We use the 'breeze' theme because it's the most beautiful
        # theme along with 'arc'
        # TODO us OS native ui; macOS : aqua
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

        # The breeze theme is missing something: there is
        # no highlight chen the user clicks on an item
        # of the Treeview. These lines add little dots
        # around the item to prevent that
        # TODO see README
        s.layout("Treeview.Item",
        [('Treeitem.padding', {'sticky': 'nswe', 'children':
            [('Treeitem.indicator', {'side': 'left', 'sticky': ''}),
            ('Treeitem.image', {'side': 'left', 'sticky': ''}),
            ('Treeitem.focus', {'side': 'left', 'sticky': '', 'children': [
                 ('Treeitem.text', {'side': 'left', 'sticky': ''}),
            ]})
            ],
        })]
        )

        # All frames of the application
        # TODO make it dynamic
        self.frames = {}

        for P in (ConnectionPage, EventsPage, EditEventPage, TicketingPage, ShowEventPage):
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

    def new_event(self):
        log.info('New event')
        self.frames['EditEventPage'].set_new_mode()
        self.show_frame('EditEventPage')


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
            pmenu.add_command(label="Log out", command=partial(self.show_frame, "ConnectionPage"))
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

        log.info(date_str)

        date = datetime.strptime(date_str, "%Y-%m-%d").date()
        return Event.select().where((Event.begin.year == date.year)
                                    & (Event.begin.month == date.month)
                                    & (Event.begin.day == date.day)).order_by(Event.begin)



    def get_categories(self):
        '''
        Return all categories
        '''
        return Category.select()


    def get_events_categories(self, event_id: int=None):
        if event_id == None:
            return [{'title':c.title, 'price':c.price, 'checked':'unchecked'} for c in Category.select()]
        else:
            ec = []
            for c in Category.select():
                checked = 'unchecked'
                if EventsCategory.select().where((EventsCategory.category == c.id) & (EventsCategory.event == event_id)):
                    checked = 'checked'
                ec.append({'title':c.title, 'price':c.price, 'checked':checked})

            return ec


    def get_projection_rooms(self):
        '''
        Return all projection rooms
        '''

        return ProjectionRoom.select()

    def get_events_per_user(self, event_id: int=None):
        if event_id == None:
            return [{'user':user.name, 'events':Team.select().where(Team.member == user).count(), 'checked':'unchecked'} for user in User.select()]
        else:
            epu = []
            for u in User.select():
                checked = 'unchecked'
                if Team.select().where((Team.member == u) & (Team.event == event_id)):
                    checked = 'checked'
                epu.append({'user':u.name, 'events':Team.select().where(Team.member == u).count(), 'checked':checked})

            return epu


    def get_users(self):
        '''
        Return all users
        '''

        return User.select()


    def update_events_page(self):
        '''
        Update the events displayed in the events page
        '''

        self.frames["EventsPage"].display_events()

    def show_frame(self, page_name: str):
        '''Show a frame for the given page name'''

        log.info('Go to frame %s' % (page_name))
        frame = self.frames[page_name]
        frame.tkraise()

        # There are some menu items/options that are only visible
        # to logged in users
        if page_name == "ConnectionPage":
            self.set_menu(False)
        else:
            self.set_menu(True)

    def check_credentials(self, login: str, password: str) -> str:
        '''
        Event raised when the user click on the login button
        on the connection page
        '''

        # We search in the database the user with the corresponding login
        u = User.select().where(User.login == login).first()

        # We check if the login is right and then the password
        if u == None:
            return 'Authentification failed : no user found'
        else:
            if password == u.password:
                self.current_user = u
                log.info("Authentification successfull")
                self.show_frame("EventsPage")
                return ''
            else:
                return 'Authentification failed : password incorrect'


    def create_event(self, event: Event) -> int:
        '''
        Create a event with a dict given in argument
        '''
        event['projection_room'] = ProjectionRoom.get(ProjectionRoom.location == event['projection_room']).id
        event['begin'] = datetime.strptime(event['begin'], "%Y-%m-%d %H:%M")
        event['responsible'] = self.current_user.id
        event_created = Event.create(**event)

        return event_created.id

    def update_event(self, event: dict, event_id: int) -> int:
        event['projection_room'] = ProjectionRoom.get(ProjectionRoom.location == event['projection_room']).id
        event['begin'] = datetime.strptime(event['begin'], "%Y-%m-%d %H:%M")
        event['responsible'] = self.current_user.id
        return Event.update(**event).where(Event.id == event_id).execute()

    def update(self, event_id: int, event: dict) -> int:
        return Event.update(**event).where(Event.id == event_id).execute()

    def get_event_by_id(self, event_id: int) -> int:
        return Event.get(Event.id == event_id)

    def update_team(self, member_names: list, event_id: int):
        log.info('Updating team for the event %d' % (event_id))
        Team.delete().where(Team.event == event_id).execute()
        self.create_team(member_names, event_id)

    def update_events_categories(self, cat_titles: list, event_id: int):
        log.info('Updating events categories for event %d' % (event_id))
        EventsCategory.delete().where(EventsCategory.event == event_id).execute()
        self.create_events_categories(cat_titles, event_id)

    def create_team(self, member_names: list, event_id: int):
        '''
        Associates a user with an event : (user, event)
        '''
        team = [{'member':User.get(User.name == name).id, 'event':event_id} for name in member_names]
        print(team)
        Team.insert_many(team).execute()

    def create_events_categories(self, cat_titles: list, event_id: int):
        '''
        Associates a category with an event
        '''
        cats = [{'category':Category.get(Category.title == title).id, 'event':event_id} for title in cat_titles]
        EventsCategory.insert_many(cats).execute()

    def delete_event(self, event_name: str) -> int:
        return Event.delete().where(Event.name == event_name).execute()

    def edit_event(self, name: str):
        event_to_edit = Event.get(Event.name == name)
        self.frames['EditEventPage'].set_edit_mode()
        self.frames['EditEventPage'].set_event(event_to_edit)
        self.frames['EditEventPage'].set_projection_room(ProjectionRoom.get(event_to_edit.projection_room))
        self.frames['EditEventPage'].set_inputs()
        self.show_frame('EditEventPage')

    def get_location(self, projection_room_id: int) -> str:
        return ProjectionRoom.get(ProjectionRoom.id == projection_room_id).location

    def get_total_seats_for_event(self, projection_room_id: int) -> int:
        return ProjectionRoom.get(ProjectionRoom.id == projection_room_id).total_seats

    def get_seats_left(self, event_id):
        event = Event.get(Event.id == event_id)
        return self.get_total_seats_for_event(event.projection_room) - event.sold_seats - event.booked_seats

    def go_to_show_event_page(self, event_name: str):
        event = Event.get(Event.name == event_name)

        self.frames['ShowEventPage'].set_event(event)
        self.frames['ShowEventPage'].set_projection_room(event.projection_room)
        self.frames['ShowEventPage'].set_categories(event.events_categories)
        self.frames['ShowEventPage'].set_responsible(event.responsible)
        self.frames['ShowEventPage'].set_members(self.get_events_members(event))
        self.frames['ShowEventPage'].set_members(event.teams)
        self.frames['ShowEventPage'].display_events_information()

        self.show_frame('ShowEventPage')

    def get_events_members(self, event):
        return User.select().join(Team).where((User.id == Team.member) & (Team.event == event))

    def go_to_ticket_page(self, event_name: str):
        event = Event.get(Event.name == event_name)

        self.frames['TicketingPage'].set_event(event)
        self.frames['TicketingPage'].set_projection_room(event.projection_room)
        self.frames['TicketingPage'].set_inputs()

        self.show_frame('TicketingPage')

    def get_categories_for_event(self, event) -> list:
        print(event.events_categories.dicts())
        return list(set([ec.category for ec in event.events_categories]))

    def has_permission_to_delete(self, event_name: str) -> bool:
        event = Event.get(Event.name == event_name)
        if event == None: return False

        return self.current_user == event.responsible


    def check_permission_to_edit(self, event_name: str) -> bool:
        event = Event.get(Event.name == event_name)
        if event == None: return False

        return Team.select().where((Team.member == self.current_user) & (Team.event == event)).count() == 1

    def app_will_quit(self):
        log.info('Application will terminate')
        log.info('Closing the database')
        db.close()
        self.destroy()


