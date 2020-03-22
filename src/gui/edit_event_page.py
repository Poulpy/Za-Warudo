import re
from tkinter import *
from tkinter import ttk
from tkcalendar import Calendar, DateEntry
from datetime import datetime
import logging as log
from gui.entry_date import EntryDate

class EditEventPage(ttk.Frame):

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller


        title = ttk.Label(self, text="Create event", font=("TkDefaultFont", "15"))
        back_button = ttk.Button(self, text='Back', command=lambda: self.controller.show_frame("EventsPage"))

        name_label = ttk.Label(self, text="Name")
        self.name_entry = ttk.Entry(self)

        # Variables to get the values after input
        self.begin_text = StringVar()
        self.hour_text = StringVar()
        self.running_time_text = StringVar()

        self.hour_text.set('12')
        self.running_time_text.set('60')

        begin = ttk.Label(self, text="Day")
        begin_entry = EntryDate(self, textvariable=self.begin_text)
        hour = ttk.Label(self, text="Hour")
        hour_entry = Spinbox(self, from_=0, to=24, textvariable=self.hour_text)
        running_time = ttk.Label(self, text="Running time (minutes)")
        running_time_entry = Spinbox(self, from_=0, to=500, textvariable=self.running_time_text)

        pj_label = ttk.Label(self, text="Projection type")
        self.projection_type_choosen = StringVar()
        projection_types = ttk.Combobox(self, textvariable=self.projection_type_choosen, state='readonly')
        projection_types['values'] = ["Film", "Documentary"]
        projection_types.current(0)

        pjs = [pj['location'] for pj in controller.get_projection_rooms().dicts()]

        pr_label = ttk.Label(self, text="Projection room")
        self.projection_room_choosen = StringVar()
        projection_rooms = ttk.Combobox(self, textvariable=self.projection_room_choosen, state='readonly')
        projection_rooms['values'] = pjs
        projection_rooms.current(0)

        room_chbutton = ttk.Checkbutton(self, text="Room reserved")
        equipment_chbutton = ttk.Checkbutton(self, text="Equipment reserved")
        management_chbutton = ttk.Checkbutton(self, text="Management reserved")
        guest_attendance_chbutton = ttk.Checkbutton(self, text="Guest attendance confirmed")

        members_label = ttk.Label(self, text="Choose members")
        user_names = [u['name'] for u in controller.get_users().dicts() if not u['is_admin']]
        members_frame = ttk.Frame(self)
        users_chbuttons = [None for i in range(len(user_names))]

        for i, user in enumerate(user_names):
            users_chbuttons[i] = ttk.Checkbutton(members_frame, text=user)
            users_chbuttons[i].grid(row=i, column=0, sticky=W)

        save_button = ttk.Button(self, text="Save", command=self.save)


        title.grid(row=0, column=0, sticky=(W+N))
        back_button.grid(row=0, column=3, sticky=E)

        name_label.grid(row=1, column=0, sticky=W)
        self.name_entry.grid(row=1, column=1)

        begin.grid(row=2, column=0, sticky=W)
        begin_entry.grid(row=2, column=1)
        hour.grid(row=3, column=0, sticky=W)
        hour_entry.grid(row=3, column=1, sticky=W)
        running_time.grid(row=3, column=2)
        running_time_entry.grid(row=3, column=3)
        pj_label.grid(row=4, column=0, sticky=W)
        projection_types.grid(row=4, column=1)
        pr_label.grid(row=4, column=2)
        projection_rooms.grid(row=4, column=3)

        room_chbutton.grid(row=5, column=0)
        equipment_chbutton.grid(row=5, column=1)
        management_chbutton.grid(row=5, column=2)
        guest_attendance_chbutton.grid(row=5, column=3)
        members_label.grid(row=6, column=0)
        members_frame.grid(row=7, column=0)
        save_button.grid(row=8, column=0)

    def save(self, event=None):
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
        self.controller.create_event(new_event)
        self.controller.update_events_page()
        self.controller.show_frame("EventsPage")

        # ^(2[0-4]|1[0-9]|[1-9])$

class Spinbox(ttk.Entry):

    def __init__(self, master=None, **kw):

        ttk.Entry.__init__(self, master, 'ttk::spinbox', **kw)

