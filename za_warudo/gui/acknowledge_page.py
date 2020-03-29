from functools import partial
from datetime import datetime
from datetime import timedelta
from tkinter import *
from tkinter import ttk
import logging as log


class AcknowledgePage(ttk.Frame):

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        self.parent = parent
        self.event_selected = None
        pad = 5


        self.events_tree = ttk.Treeview(self, columns=('Date', 'Hour'), selectmode='browse')
        self.events_tree.column("Date", anchor='center')
        self.events_tree.column("Hour", anchor='center')
        self.events_tree.heading("#0", text="Name")
        self.events_tree.heading("Date", text="Begin")
        self.events_tree.heading("Hour", text="End")
        self.display_events()

        self.events_tree.tag_configure('odd', background="#F0F0F0")
        self.events_tree.tag_configure('even', background="#FAFAFA")

        self.events_tree.bind('<<TreeviewSelect>>', self.select_event)
        ack_button = ttk.Button(self, text="Acknowledge", command=self.ack_event)

        #self.events_tree.grid(row=0, column=0, sticky=NSEW)
        #ack_button.grid(row=1, column=0, sticky=NSEW)
        self.events_tree.pack(side=TOP, fill=BOTH, expand=True)
        ack_button.pack()

    def ack_event(self):
        if self.event_selected != None:
            log.info('ACK EVENT %s' % (self.event_name))
            print(self.event_name)
            self.controller.ack_event(self.event_name)
            self.display_events()

    def display_events(self):
        '''
        Show the events according to the date of the input
        '''

        self.events_tree.delete(*self.events_tree.get_children())
        events = self.controller.get_events_for_user_to_be_ack()
        print(events)
        if len(events) == 0: return
        print(events[0])

        for i, event in enumerate(events[0]):
            if i % 2 == 0:
                tag = 'odd'
            else:
                tag = 'even'
            date = event.begin.strftime("%H:%M"),
            hour = event.begin.strftime("%H:%M") + ':' + (event.begin + timedelta(minutes=event.running_time)).strftime("%H:%M")
            self.events_tree.insert("", 'end', text=event.name, values=(date, hour), tags=(tag))



    def select_event(self, event=None):
        self.event_selected = event.widget.selection()
        self.event_name = self.events_tree.item(self.event_selected)['text']

