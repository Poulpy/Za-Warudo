from datetime import datetime
from tkinter import *
from tkinter import ttk
import logging as log
import re

import ttkwidgets as tkw
from tkcalendar import Calendar, DateEntry

from gui.entry_date import EntryDate

class EditEventPage(ttk.Frame):
    '''
    Frame to create a new event
    Upon creation the user is redirected to the events page
    TODO frame to create AND edit an event
    '''

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        title = ttk.Label(self, text="Create event", font=("TkDefaultFont", "15"))
        back_button = ttk.Button(self, text='Back', command=lambda: self.controller.show_frame("EventsPage"))

        # Event form
        name_label = ttk.Label(self, text="Name")
        self.name_entry = ttk.Entry(self)

        # Variables to get the values after input
        self.begin_text = StringVar()
        self.hour_text = StringVar()
        self.running_time_text = StringVar()

        self.hour_text.set('12')
        self.running_time_text.set('60')

        # Input for the date of the event
        begin = ttk.Label(self, text="Day")
        begin_entry = EntryDate(self, textvariable=self.begin_text)
        # Input for the hour of the event
        hour = ttk.Label(self, text="Hour")
        hour_entry = Spinbox(self, from_=0, to=24, textvariable=self.hour_text)
        # Input for the running time, in minutes
        # TODO actually we can type anything in this s* widget
        # do something to prevent that by using regex
        # When clicking on the save button, there may be a label
        # if the input is wrong
        running_time = ttk.Label(self, text="Running time (minutes)")
        running_time_entry = Spinbox(self, from_=0, to=500, textvariable=self.running_time_text)

        # Dropdown list for the type of the projection (film, docu)
        pj_label = ttk.Label(self, text="Projection type")
        self.projection_type_choosen = StringVar()
        projection_types = ttk.Combobox(self, textvariable=self.projection_type_choosen, state='readonly')
        projection_types['values'] = ["Film", "Documentary"]
        projection_types.current(0)

        pjs = [pj['location'] for pj in controller.get_projection_rooms().dicts()]

        # Dropdown list for the location of the event
        pr_label = ttk.Label(self, text="Projection room")
        self.projection_room_choosen = StringVar()
        projection_rooms = ttk.Combobox(self, textvariable=self.projection_room_choosen, state='readonly')
        projection_rooms['values'] = pjs
        projection_rooms.current(0)

        # Inputs for the event's status to go 'finished'
        check_frame = ttk.Frame(self)
        room_chbutton = ttk.Checkbutton(check_frame, text="Room reserved")
        equipment_chbutton = ttk.Checkbutton(check_frame, text="Equipment reserved")
        management_chbutton = ttk.Checkbutton(check_frame, text="Management reserved")
        guest_attendance_chbutton = ttk.Checkbutton(check_frame, text="Guest attendance confirmed")


        # TODO the user can assign users to this event
        members_label = ttk.Label(self, text="Add members")
        user_names = [u['name'] for u in controller.get_users().dicts() if not u['is_admin']]

        # List of users; the responsible has to choose among them
        # members that'll participate in the event's organisation
        self.members_tree = tkw.CheckboxTreeview(self, columns=('Events'), selectmode='browse')
        self.members_tree.column("Events", width=50)
        self.members_tree.heading("#0", text="Name")
        self.members_tree.heading("Events", text="Events")

        self.members_tree.tag_configure('odd', background="#F0F0F0")
        self.members_tree.tag_configure('even', background="#FAFAFA")
        for i, user in enumerate(user_names):
            self.members_tree.insert('', 'end', text=user, tags=('even' if i % 2 else 'odd',))

        # CATEGORIES
        categories_label = ttk.Label(self, text="Add categories")
        categories = controller.get_categories().dicts()

        self.cats_tree = tkw.CheckboxTreeview(self, columns=('Price'), selectmode='none')
        self.cats_tree.column("#0", width=100)
        self.cats_tree.column("Price", width=50)
        self.cats_tree.heading("#0", text="Title")
        self.cats_tree.heading("Price", text="Price")

        self.cats_tree.tag_configure('odd', background="#F0F0F0")
        self.cats_tree.tag_configure('even', background="#FAFAFA")

        for i, category in enumerate(categories):
            self.cats_tree.insert('', 'end', text=category['title'], tags=('even' if i % 2 else 'odd',), values=(str(category['price']) + " €"))

        # And of course, the button to save it all
        save_button = ttk.Button(self, text="Save", command=self.save)


        # Placing the components
        # ROW 0
        title.grid(row=0, column=0, sticky=(W+N))
        back_button.grid(row=0, column=3, sticky=E)

        # ROW 1
        name_label.grid(row=1, column=0, sticky=W, pady=5, padx=5)
        self.name_entry.grid(row=1, column=1, pady=5, padx=5, sticky=E)

        # ROW 2
        begin.grid(row=2, column=0, sticky=W, pady=5, padx=5)
        begin_entry.grid(row=2, column=1, sticky=E, pady=5, padx=5)
        hour.grid(row=2, column=2, sticky=W, pady=5, padx=5)
        hour_entry.grid(row=2, column=3, sticky=E, pady=5, padx=5)

        # ROW 3
        running_time.grid(row=3, column=0, pady=5, padx=5, sticky=W)
        running_time_entry.grid(row=3, column=1, pady=5, padx=5, sticky=E)

        # ROW 4
        pj_label.grid(row=4, column=0, sticky=W, pady=5, padx=5)
        projection_types.grid(row=4, column=1, sticky=E, pady=5, padx=5)
        pr_label.grid(row=4, column=2, pady=5, sticky=W, padx=5)
        projection_rooms.grid(row=4, column=3, sticky=E, pady=5, padx=5)

        # ROW 5
        check_frame.grid(row=7, column=2, rowspan=2, columnspan=2, sticky=N+W)
        room_chbutton.grid(row=5, column=2, sticky=W)
        equipment_chbutton.grid(row=6, column=2, sticky=W)
        management_chbutton.grid(row=7, column=2, sticky=W)
        guest_attendance_chbutton.grid(row=8, column=2, sticky=W)

        # ROW 6
        members_label.grid(row=5, column=0, pady=5, padx=5, sticky=W)
        self.members_tree.grid(row=6, column=0, columnspan=2, pady=5, padx=5, sticky=W)
        categories_label.grid(row=5, column=2, pady=5, padx=5, sticky=W)
        self.cats_tree.grid(row=6, column=2, columnspan=2, pady=5, padx=5, sticky=W)

        save_button.grid(row=8, column=0, pady=5, padx=5, sticky=W)

    def save(self, event=None):
        '''
        Get all the datas from the form to create an
        event. Redirects to the events page
        '''
        new_event = dict()

        log.info("Name " + self.name_entry.get())
        log.info("Day " + self.begin_text.get())
        log.info("Hour " + self.hour_text.get())
        log.info("Running time " + self.running_time_text.get())
        '''
        p = re.compile('^(2[0-4]|1[0-9]|[1-9])$')
        if p.match(self.hour_text.get()) == None:
            print("Wrong hour format")
        '''

        log.info("Projection type " + self.projection_type_choosen.get())
        log.info("Projection room " + self.projection_room_choosen.get())

        new_event['name'] = self.name_entry.get()
        new_event['begin'] = self.begin_text.get() + ' ' + self.hour_text.get() + ':00'
        new_event['running_time'] = self.running_time_text.get()
        new_event['projection_type'] = self.projection_type_choosen.get()
        new_event['projection_room'] = self.projection_room_choosen.get()
        member_names = [self.members_tree.item(member)['text'] for member in self.members_tree.get_checked()]
        event_id = self.controller.create_event(new_event)

        self.controller.create_team(member_names, event_id)
        self.controller.update_events_page()
        self.controller.show_frame("EventsPage")

        # ^(2[0-4]|1[0-9]|[1-9])$

class Spinbox(ttk.Entry):

    def __init__(self, master=None, **kw):

        ttk.Entry.__init__(self, master, 'ttk::spinbox', **kw)

