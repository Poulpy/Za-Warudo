from functools import partial
from datetime import datetime
from datetime import timedelta
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import logging as log

from tkcalendar import Calendar, DateEntry

from gui.widgets import EntryDate
from gui.acknowledge_page import AcknowledgePage

# TODO put in module frames
class EventsPage(ttk.Frame):
    '''
    Frame showing all events of a day. With the
    right permissions, the user can :
    - delete an event
    - show some details
    - modify
    - see the ticketing page
    - create an event
    '''

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        self.event_selected = None
        pad = 5

        self.notification_text = StringVar()
        title = ttk.Label(self, text="Events", font=("TkDefaultFont", "15"))
        notification = ttk.Label(self, textvariable=self.notification_text)

        # Creation of of an event : clicking on that button
        # will redirect the user on the edit event frame

        self.date_text = StringVar()
        date_entry = EntryDate(self, textvariable=self.date_text)
        self.date_text.set(datetime.now().strftime("%Y-%m-%d"))
        # Each time the date changes, the events of the
        # date in the input are shown
        self.date_text.trace('w', lambda name, index, mode, date_text=self.date_text: self.display_events())

        new_event_button = ttk.Button(self, text="New event", command=self.controller.new_event)
        edit_button = ttk.Button(self, text="Edit", command=self.edit_event)
        show_button = ttk.Button(self, text="Details", command=self.link_to_show_page)
        delete_button = ttk.Button(self, text="Delete", command=self.confirm_delete)
        ticket_button = ttk.Button(self, text="Ticketing", command=self.link_to_ticketing_page)


        # The events are shown in a table. The columns shows:
        # the name, the date the event starts, the date the event
        # ends, and the type of the projection
        self.events_tree = ttk.Treeview(self, columns=('Begin', 'End', 'Type', 'Place', 'Seats'), selectmode='browse')
        self.events_tree.column("Begin", width=20, anchor='center')
        self.events_tree.column("End", width=20, anchor='center')
        self.events_tree.column("Type", width=20, anchor='center')
        self.events_tree.column("Place", width=20, anchor='center')
        self.events_tree.column("Seats", width=20, anchor='center')
        self.events_tree.heading("#0", text="Name")
        self.events_tree.heading("Begin", text="Begin")
        self.events_tree.heading("End", text="End")
        self.events_tree.heading("Type", text="Type")
        self.events_tree.heading("Place", text="Place")
        self.events_tree.heading("Seats", text="Seats left")
        self.display_events()

        self.events_tree.tag_configure('odd', background="#F0F0F0")
        self.events_tree.tag_configure('even', background="#FAFAFA")

        self.events_tree.bind('<<TreeviewSelect>>', self.select_event)



        title.grid(row=0, column=0, sticky=(W+N))
        new_event_button.grid(row=0, column=1, sticky=(W+E), pady=5, padx=5)

        self.events_tree.grid(row=1, column=0, rowspan=5, sticky=NSEW)
        date_entry.grid(row=1, column=1, sticky=(W+E), pady=5, padx=5)

        edit_button.grid(row=2, column=1, sticky=(W+E), pady=5, padx=5)
        show_button.grid(row=3, column=1, sticky=(W+E), pady=5, padx=5)
        delete_button.grid(row=4, column=1, sticky=(W+E), pady=5, padx=5)
        ticket_button.grid(row=5, column=1, sticky=(W+E), pady=5, padx=5)

        notification.grid(row=6, column=0, columnspan=2, sticky=W, padx=pad, pady=pad)

        self.grid_columnconfigure(0, weight=2)

    def select_event(self, event=None):
        self.event_selected = event.widget.selection()
        self.event_name = self.events_tree.item(self.event_selected)['text']

    def display_events(self):
        '''
        Show the events according to the date of the input
        '''

        events = self.controller.get_events(self.date_text.get())
        self.events_tree.delete(*self.events_tree.get_children())

        for i, event in enumerate(events):
            if i % 2 == 0:
                tag = 'odd'
            else:
                tag = 'even'
            values = (event.begin.strftime("%H:%M"),
                      (event.begin + timedelta(minutes=event.running_time)).strftime("%H:%M"),
                      event.projection_type,
                      self.controller.get_location(event.projection_room),
                      self.controller.get_seats_left(event.id))
            self.events_tree.insert("", 'end', text=event.name, values=values, tags=(tag))

    def edit_event(self):
        '''
        Redirect to the edit page, if an event is selected
        '''
        if self.event_selected != None:
            if self.controller.has_permission_to_edit(self.event_name) and self.controller.get_events_status(self.event_name) != 'finished':
                log.info('Edit of event %s' % (self.event_name))
                self.controller.edit_event(name=self.event_name)
            else:
                self.notification_text.set("You don't have the permission to edit this event")
        else:
            self.notification_text.set('No event selected')

    def confirm_delete(self):
        '''
        Pop up window to confirm an event deletion
        '''
        if self.event_selected != None:
            if self.controller.has_permission_to_delete(self.event_name):
                log.info('Confirm delete of event %s' % (self.event_name))
                rst = messagebox.askquestion("Confirm", "Are you sure you want to delete this event ?")
                if rst == 'yes':
                    self.controller.update_events_page()
            else:
                self.notification_text.set("You don't have the permission to delete this event. Please contact the manager")
        else:
            self.notification_text.set('No event selected')

    def link_to_ticketing_page(self):
        '''
        Redirect to the ticketing page of an event The event must be
        'finished'
        '''
        if self.event_selected != None:
            if self.controller.has_permission_to_edit(self.event_name):
                if self.controller.get_events_status(self.event_name) == 'finished':
                    self.controller.go_to_ticket_page(event_name=self.event_name)
                else:
                    self.notification_text.set('This event is not yet finished')
            else:
                self.notification_text.set("You don't have the permission to edit this event")
        else:
            self.notification_text.set('No event selected')
            log.info('No item selected')

    def link_to_show_page(self):
        '''
        Redirect to the details page, if an event is selected
        '''
        if self.event_selected != None:
            self.controller.go_to_show_event_page(event_name=self.event_name)
        else:
            self.notification_text.set('No event selected')
            log.info('No item selected')

    def pop_ack_page(self):
        '''
        Pop up where the user can acknowledge events
        acknowledge == change status
        '''
        top = Toplevel(self)
        top.geometry('700x400')
        top.title('Change status of events')

        ack_page = AcknowledgePage(top, self.controller)
        ack_page.pack(fill=BOTH, expand=True)


    def display_ack_button(self):
        '''
        The 'acknowledge' button appears IF there are events to be
        acknowledged by the user
        '''
        ack_button = ttk.Button(self, text="Acknowledge", command=self.pop_ack_page)
        if len(self.controller.get_events_for_user_to_be_ack()) != 0:
            ack_button.grid(row=6, column=1, sticky=W+E, pady=5, padx=5)

