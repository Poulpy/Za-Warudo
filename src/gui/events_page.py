from datetime import datetime
from datetime import timedelta
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import logging as log

from tkcalendar import Calendar, DateEntry

from gui.entry_date import EntryDate

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

        title = ttk.Label(self, text="Events", font=("TkDefaultFont", "15"))

        # Creation of of an event : clicking on that button
        # will redirect the user on the edit event frame
        new_event_button = ttk.Button(self, text="New event", command=lambda: controller.show_frame("EditEventPage"))

        self.date_text = StringVar()
        self.date_entry = EntryDate(self, textvariable=self.date_text)
        self.date_label = ttk.Label(self, textvariable=self.date_text)
        self.date_text.set(datetime.now().strftime("%Y-%m-%d"))
        # Each time the date changes, the events of the
        # date in the input are shown
        self.date_text.trace('w', lambda name, index, mode, date_text=self.date_text: self.set_displayed_events())

        ttk.Button(self, text="Edit").grid(row=2, column=1, sticky=(W+E), pady=5, padx=5)
        ttk.Button(self, text="Details").grid(row=3, column=1, sticky=(W+E), pady=5, padx=5)
        ttk.Button(self, text="Delete", command=self.confirm_delete).grid(row=4, column=1, sticky=(W+E), pady=5, padx=5)
        ttk.Button(self, text="Ticketing").grid(row=5, column=1, sticky=(W+E), pady=5, padx=5)


        # The events are shown in a table. The columns shows:
        # the name, the date the event starts, the date the event
        # ends, and the type of the projection
        self.events_tree = ttk.Treeview(self, columns=('Begin', 'End', 'Type'), selectmode='browse')
        self.events_tree.column("Begin", width=50)
        self.events_tree.column("End", width=50)
        self.events_tree.column("Type", width=50)
        self.events_tree.heading("#0", text="Name")
        self.events_tree.heading("Begin", text="Begin")
        self.events_tree.heading("End", text="End")
        self.events_tree.heading("Type", text="Type")
        self.set_displayed_events()

        self.events_tree.tag_configure('odd', background="#F0F0F0")
        self.events_tree.tag_configure('even', background="#FAFAFA")
        self.events_tree.tag_configure('select')

        self.events_tree.tag_bind('select', '<Button-1>', self.item_clicked)

        style = ttk.Style()

        # The breeze theme is missing something: there is
        # no highlight chen the user clicks on an item
        # of the Treeview. These lines add little dots
        # around the item to prevent that
        # TODO see README
        style.layout("Treeview.Item",
        [('Treeitem.padding', {'sticky': 'nswe', 'children':
            [('Treeitem.indicator', {'side': 'left', 'sticky': ''}),
            ('Treeitem.image', {'side': 'left', 'sticky': ''}),
            ('Treeitem.focus', {'side': 'left', 'sticky': '', 'children': [
                 ('Treeitem.text', {'side': 'left', 'sticky': ''}),
            ]})
            ],
        })]
        )

        title.grid(row=0, column=0, sticky=(W+N))
        new_event_button.grid(row=0, column=1, sticky=(W+E), pady=5, padx=5)
        self.date_entry.grid(row=1, column=1, sticky=(W+E), pady=5, padx=5)
        self.events_tree.grid(row=1, column=0, rowspan=5, sticky=NSEW)
        self.grid_columnconfigure(0, weight=2)


    def item_clicked(self, event=None):
        print('item clicked')
        it = self.events_tree.focus()
        self.events_tree.focus(it)
        self.events_tree.selection_set(it)

    def set_displayed_events(self):
        '''
        Show the events according to the date of the input
        '''

        events = self.controller.get_events(self.date_text.get())

        self.events_tree.delete(*self.events_tree.get_children())
        for i, event in enumerate(events.dicts()):
            if i % 2 == 0:
                tag = 'odd'
            else:
                tag = 'even'
            tid = self.events_tree.insert("", 'end', text=event['name'],
                                          values=(event['begin'].strftime("%H:%M"),
                                                  (event['begin'] + timedelta(minutes=event['running_time'])).strftime("%H:%M"),
                                                  event['projection_type']), tags=(tag, 'select'))

    def confirm_delete(self):
        '''
        Pop up window to confirm an event deletion
        '''
        messagebox.askquestion("Confirm", "Are you sure you want to delete this event ?")


