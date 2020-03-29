from functools import partial
from datetime import datetime
from datetime import timedelta
from tkinter import *
from tkinter import ttk
import logging as log


class AcknowledgePage(ttk.Frame):
    '''
    This page contains all events that needs to be
    acknowledged by a member of the event.
    It changes the status of the event, 'created'
    to 'in progress'
    '''

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        self.parent = parent
        self.event_selected = None
        pad = 5


        # Treeview containing events with a status 'created'
        # You can see the name, day, the hour the event begins
        # and the hour the event ends
        self.events_tree = ttk.Treeview(self, columns=('Date', 'Hour'), selectmode='browse')
        self.events_tree.column("Date", anchor='center')
        self.events_tree.column("Hour", anchor='center')
        self.events_tree.heading("#0", text="Name")
        self.events_tree.heading("Date", text="Begin")
        self.events_tree.heading("Hour", text="End")
        # We fill the treeview with datas
        self.display_events()

        # The rows are grey/white alternatively
        self.events_tree.tag_configure('odd', background="#F0F0F0")
        self.events_tree.tag_configure('even', background="#FAFAFA")

        self.events_tree.bind('<<TreeviewSelect>>', self.select_event)
        ack_button = ttk.Button(self, text="Acknowledge", command=self.ack_event)

        self.events_tree.pack(side=TOP, fill=BOTH, expand=True)
        ack_button.pack()

    def ack_event(self):
        '''
        Changes the status of the event from 'created
        to 'in progress'
        '''

        if self.event_selected != None:
            log.info('ACK EVENT %s' % (self.event_name))
            self.controller.ack_event(self.event_name)
            self.display_events()

    def display_events(self):
        '''
        Fill the treeview with events
        '''

        self.events_tree.delete(*self.events_tree.get_children())
        events = self.controller.get_events_for_user_to_be_ack()
        if len(events) == 0: return

        for i, event in enumerate(events[0]):
            if i % 2 == 0:
                tag = 'odd'
            else:
                tag = 'even'
            date = event.begin.strftime("%H:%M"),
            hour = (event.begin.strftime("%H:%M"),
                    ':',
                    (event.begin + timedelta(minutes=event.running_time)).strftime("%H:%M"))
            self.events_tree.insert("", 'end', text=event.name, values=(date, hour), tags=(tag))



    def select_event(self, event=None):
        '''
        Tkinter event triggered when a user clicks on a row of the treeview
        '''
        self.event_selected = event.widget.selection()
        self.event_name = self.events_tree.item(self.event_selected)['text']

