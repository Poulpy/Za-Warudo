from functools import partial
from datetime import datetime
from datetime import timedelta
from tkinter import *
from tkinter import ttk
import logging as log

class ShowEventPage(ttk.Frame):
    '''
    Page showing details about and event
    '''

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        self.event = None
        self.projection_room = None

        pricelist_frame = ttk.Frame(self)
        members_frame = ttk.Frame(self)

        # Default padding for the widgets
        pad = 10
        mut_labels = ('name', 'projection_type', 'location',
                      'date', 'seats_left', 'sold_seats',
                      'booked_seats', 'responsible')

        label = dict()
        self.textvar = dict()
        value = dict()

        for var in mut_labels:
            label[var] = ttk.Label(self, text=var.capitalize().replace('_', ' '))
            self.textvar[var] = StringVar()
            value[var] = ttk.Label(self, textvariable=self.textvar[var])

        # Buttons
        back_button = ttk.Button(self, text="Back", command=self.back)
        timetable_button = ttk.Button(self, text="Timetable", command=self.timetable)

        # Treeviews
        label['members'] = ttk.Label(self, text="Members")
        members_scrollbar = ttk.Scrollbar(members_frame, orient=VERTICAL)
        self.members_tree = ttk.Treeview(members_frame, selectmode='browse', yscrollcommand=members_scrollbar.set)
        self.members_tree.heading("#0", text="Name")
        self.members_tree.tag_configure('odd', background="#F0F0F0")
        self.members_tree.tag_configure('even', background="#FAFAFA")
        members_scrollbar.configure(command=self.members_tree.yview)
        self.members_tree.pack(side=LEFT)
        members_scrollbar.pack()

        label['pricelist'] = ttk.Label(self, text="Price list")
        pricelist_scrollbar = ttk.Scrollbar(pricelist_frame, orient=VERTICAL)
        self.pricelist_tree = ttk.Treeview(pricelist_frame, columns=("#1"), yscrollcommand=members_scrollbar.set)
        self.pricelist_tree.heading("#0", text="Title")
        self.pricelist_tree.heading("#1", text="Price")
        self.pricelist_tree.column("#1", width=50)
        self.pricelist_tree.tag_configure('odd', background="#F0F0F0")
        self.pricelist_tree.tag_configure('even', background="#FAFAFA")
        pricelist_scrollbar.configure(command=self.pricelist_tree.yview)
        self.pricelist_tree.pack(side=LEFT)
        pricelist_scrollbar.pack()

        # Grid
        back_button.grid(row=0, column=6, padx=pad, pady=pad)

        label['name'].grid(row=1, column=0, padx=pad, pady=pad, sticky=W)
        value['name'].grid(row=1, column=1, padx=pad, pady=pad, sticky=E)
        label['seats_left'].grid(row=1, column=2, padx=pad, pady=pad, sticky=W)
        value['seats_left'].grid(row=1, column=3, padx=pad, pady=pad, sticky=W)
        label['members'].grid(row=1, column=4, padx=pad, pady=pad, sticky=W)
        label['pricelist'].grid(row=1, column=5, padx=pad, pady=pad, sticky=W)

        label['projection_type'].grid(row=2, column=0, padx=pad, pady=pad, sticky=W)
        value['projection_type'].grid(row=2, column=1, padx=pad, pady=pad, sticky=E)
        label['sold_seats'].grid(row=2, column=2, padx=pad, pady=pad, sticky=W)
        value['sold_seats'].grid(row=2, column=3, padx=pad, pady=pad, sticky=W)
        members_frame.grid(row=2, column=4, rowspan=9, padx=pad, pady=pad, sticky=NSEW)
        pricelist_frame.grid(row=2, column=5, rowspan=9, padx=pad, pady=pad, sticky=NSEW)

        label['location'].grid(row=3, column=0, padx=pad, pady=pad, sticky=W)
        value['location'].grid(row=3, column=1, padx=pad, pady=pad, sticky=E)
        label['booked_seats'].grid(row=3, column=2, padx=pad, pady=pad, sticky=W)
        value['booked_seats'].grid(row=3, column=3, padx=pad, pady=pad, sticky=W)

        label['date'].grid(row=4, column=0, padx=pad, pady=pad, sticky=W)
        value['date'].grid(row=4, column=1, padx=pad, pady=pad, sticky=E)
        label['responsible'].grid(row=4, column=2, padx=pad, pady=pad, sticky=W)
        value['responsible'].grid(row=4, column=3, padx=pad, pady=pad, sticky=W)

    def display_events_information(self):
        # day-month-year begin_hour - end_hour
        date = self.event.begin.strftime("%d-%m-%Y %H")
        date += 'h - '
        date += (self.event.begin + timedelta(minutes=self.event.running_time)).strftime("%H")
        date += 'h'
        seats_left = str(self.projection_room.total_seats - self.event.booked_seats - self.event.sold_seats)
        seats_left += ' / ' + str(self.projection_room.total_seats)
        revenue = str(self.event.revenue) + ' €'
        self.textvar['name'].set(self.event.name)
        self.textvar['projection_type'].set(self.event.projection_type)
        self.textvar['location'].set(self.projection_room.location)
        self.textvar['date'].set(date)
        self.textvar['seats_left'].set(seats_left)
        self.textvar['sold_seats'].set(self.event.sold_seats)
        self.textvar['booked_seats'].set(self.event.booked_seats)
        self.textvar['responsible'].set(self.responsible.name)
        self.display_members()
        self.display_pricelist()
        #print(self.members)


    def timetable(self):
        pass

    def back(self):
        self.controller.show_frame('EventsPage')

    def display_pricelist(self):
        self.pricelist_tree.delete(*self.pricelist_tree.get_children())

        print(self.categories)
        for i, price in enumerate(self.categories):
            value = str(price.category.price) + ' €'
            self.pricelist_tree.insert('', 'end', text=price.category.title, values=(value,), tags=('even' if i % 2 else 'odd',))


    def display_members(self):
        self.members_tree.delete(*self.members_tree.get_children())

        #print('Members')
        #print(len(self.members))
        for i, team in enumerate(self.members):
            #log.info('iid : %d, member : %s' % (i, team.member.name))
            self.members_tree.insert('', 'end', iid=str(i), text=team.member.name, tags=('even' if i % 2 else 'odd',))

    def display_event_information(self):
        pass

    def set_event(self, event):
        self.event = event

    def set_projection_room(self, projection_room):
        self.projection_room = projection_room

    def set_categories(self, categories):
        self.categories = categories

    def set_responsible(self, responsible):
        self.responsible = responsible

    def set_members(self, members):
        self.members = members


