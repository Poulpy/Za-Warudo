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


        title.grid(row=0, column=0, sticky=(W+N))
        back_button.grid(row=0, column=2, sticky=E)

        name_label.grid(row=1, column=0)
        self.name_entry.grid(row=1, column=1)

        begin.grid(row=2, column=0)
        self.begin_entry.grid(row=2, column=1)
        end.grid(row=3, column=0)
        self.end_entry.grid(row=3, column=1)

