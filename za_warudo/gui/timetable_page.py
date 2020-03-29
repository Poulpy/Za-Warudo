from functools import partial
from datetime import datetime
from datetime import timedelta
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import logging as log

from tkcalendar import Calendar, DateEntry

from gui.widgets import EntryDate

class TimetablePage(ttk.Frame):

    def __init__(self, parent, events):
        ttk.Frame.__init__(self, parent)
        self.events = events

        self.events_tree = ttk.Treeview(self, columns=('Begin', 'End'), selectmode='none')
        #self.events_tree.column("Date", width=70, anchor='center')
        self.events_tree.column("Begin", width=50, anchor='center')
        self.events_tree.column("End", width=50, anchor='center')
        self.events_tree.heading("#0", text="Name")
        #self.events_tree.heading("Date", text="Date")
        self.events_tree.heading("Begin", text="Begin")
        self.events_tree.heading("End", text="End")
        self.display_events()

        self.events_tree.tag_configure('odd', background="#F0F0F0")
        self.events_tree.tag_configure('even', background="#FAFAFA")

        self.events_tree.pack(expand=True, fill=BOTH)

    def display_events(self):
        '''
        Show the events according to the date of the input
        '''

        for i, event in enumerate(self.events):
            if i % 2 == 0:
                tag = 'odd'
            else:
                tag = 'even'
            values = (event['begin'], event['end'])
            self.events_tree.insert("", 'end', text=event['name'], values=values, tags=(tag))

