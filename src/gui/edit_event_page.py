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

        self.begin_text = StringVar()
        self.end_text = StringVar()
        begin = ttk.Label(self, text="Begin date")
        self.begin_entry = EntryDate(self, textvariable=self.begin_text)
        end = ttk.Label(self, text="End date")
        self.end_entry = EntryDate(self, textvariable=self.end_text)

        pj_label = ttk.Label(self, text="Projection type")
        self.projection_type_choosen = StringVar()
        projection_types = ttk.Combobox(self, textvariable=self.projection_type_choosen, state='readonly')
        projection_types['values'] = ["Film",
                                      "Documentary"]
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
        self.begin_entry.grid(row=2, column=1)
        end.grid(row=3, column=0, sticky=W)
        self.end_entry.grid(row=3, column=1)
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
        log.info("Name " + self.name_entry.get())
        log.info("Begin " + self.begin_text.get())
        log.info("End " + self.end_text.get())
        log.info("Projection type " + self.projection_type_choosen.get())
        log.info("Projection room " + self.projection_room_choosen.get())

