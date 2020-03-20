from tkinter import *
from tkinter import ttk
from tkcalendar import Calendar, DateEntry
from datetime import datetime
import logging as log
from gui.entry_date import EntryDate

class EventsPage(ttk.Frame):

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        title = ttk.Label(self, text="Events", font=("TkDefaultFont", "15"))

        new_event_button = ttk.Button(self, text="New event", command=lambda: controller.show_frame("EditEventPage"))

        title.grid(row=0, column=0, sticky=(W+N))
        new_event_button.grid(row=0, column=1, sticky=(W+E), pady=5, padx=5)

        self.date_text = StringVar()
        self.date_entry = EntryDate(self, textvariable=self.date_text)
        self.date_label = ttk.Label(self, textvariable=self.date_text)
        self.date_text.set(datetime.now().strftime("%Y-%m-%d"))
        self.date_text.trace('w', lambda name, index, mode, date_text=self.date_text: self.set_displayed_events())

        self.date_entry.grid(row=1, column=1, sticky=(W+E), pady=5, padx=5)
        ttk.Button(self, text="Edit").grid(row=2, column=1, sticky=(W+E), pady=5, padx=5)
        ttk.Button(self, text="Details").grid(row=3, column=1, sticky=(W+E), pady=5, padx=5)
        ttk.Button(self, text="Delete").grid(row=4, column=1, sticky=(W+E), pady=5, padx=5)
        ttk.Button(self, text="Ticketing").grid(row=5, column=1, sticky=(W+E), pady=5, padx=5)


        # self.date_label.grid(row=1, column=2, sticky=W)

        self.grid_columnconfigure(0, weight=2)



        events = self.controller.get_events(self.date_text.get())

        self.events_tree = ttk.Treeview(self, columns=('Begin', 'End', 'Type'), selectmode='browse')
        self.events_tree.column("Begin", width=50)
        self.events_tree.column("End", width=50)
        self.events_tree.column("Type", width=50)
        self.events_tree.heading("#0", text="Name")
        self.events_tree.heading("Begin", text="Begin")
        self.events_tree.heading("End", text="End")
        self.events_tree.heading("Type", text="Type")
        for i, event in enumerate(events.dicts()):
            if i % 2 == 0:
                tag = 'odd'
            else:
                tag = 'even'
            tid = self.events_tree.insert("", 'end', text=event['name'],
                                          values=(event['begin'].strftime("%H:%M"), event['end'].strftime("%H:%M"),
                                          event['projection_type']), tags=(tag, 'select'))

        self.events_tree.tag_configure('odd', background="#F0F0F0")
        self.events_tree.tag_configure('even', background="#FAFAFA")
        self.events_tree.tag_configure('select')

        self.events_tree.tag_bind('select', '<Button-1>', self.item_clicked)
        self.events_tree.grid(row=1, column=0, rowspan=5, sticky=NSEW)

        style = ttk.Style()

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

    def item_clicked(self, event=None):
        print('item clicked')
        it = self.events_tree.focus()
        self.events_tree.focus(it)
        self.events_tree.selection_set(it)

    def tree_select(self, event=None):
        item = self.events_tree.selection()[0]
        print(item)
        self.events_tree.focus(item)
        #self.events_tree.item(item, tags='blue')

    def display_events(self, top, cal):
        log.info(self.controller.get_events(self.date_text.get()))

    def set_displayed_events(self):
        events = self.controller.get_events(self.date_text.get())

        self.events_tree.delete(*self.events_tree.get_children())
        for i, event in enumerate(events.dicts()):
            if i % 2 == 0:
                tag = 'odd'
            else:
                tag = 'even'
            tid = self.events_tree.insert("", 'end', text=event['name'],
                                          values=(event['begin'].strftime("%H:%M"), event['end'].strftime("%H:%M"),
                                          event['projection_type']), tags=(tag, 'select'))

