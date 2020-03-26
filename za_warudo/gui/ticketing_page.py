from datetime import datetime
from datetime import timedelta
from tkinter import *
from tkinter import ttk
import logging as log

class TicketingPage(ttk.Frame):
    '''
    Page to book or sell tickets
    '''

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        self.event = None
        self.projection_room = None

        # Default padding for the widgets
        pad = 5

        labels = dict()
        self.textvar = dict()

        for var in ('name', 'projection_type', 'date', 'seats_left', 'sold_seats', 'booked_seats', 'revenue'):
            self.textvar[var] = StringVar()
            labels[var] = ttk.Label(self, text=var.capitalize().replace('_', ' '))

        tickets_frame = ttk.Frame(self)

        back_button = ttk.Button(self, text='Back', command=self.back)
        sell_button = ttk.Button(self, text='Sell', command=self.sell)
        book_button = ttk.Button(self, text='Book', command=self.book)

        # Those labels can be changed
        event_name_label = ttk.Label(self, textvariable=self.textvar['name'])
        event_type_label = ttk.Label(self, textvariable=self.textvar['projection_type'])
        event_date_label = ttk.Label(self, textvariable=self.textvar['date'])
        seats_left_label = ttk.Label(self, textvariable=self.textvar['seats_left'])
        seats_sold_label = ttk.Label(self, textvariable=self.textvar['sold_seats'])
        seats_booked_label = ttk.Label(self, textvariable=self.textvar['booked_seats'])
        revenue_label = ttk.Label(self, textvariable=self.textvar['revenue'])

        # GRID
        event_name_label.grid(row=0, column=0, padx=pad, pady=pad)
        event_type_label.grid(row=0, column=1, padx=pad, pady=pad)
        back_button.grid(row=0, column=4, padx=pad, pady=pad)

        # labels['date'].grid(row=1, column=0, padx=pad, pady=pad, sticky=W)
        event_date_label.grid(row=1, column=1, padx=pad, pady=pad, sticky=E)

        labels['seats_left'].grid(row=2, column=0, padx=pad, pady=pad, sticky=W)
        seats_left_label.grid(row=2, column=1, padx=pad, pady=pad, sticky=E)

        labels['sold_seats'].grid(row=3, column=0, padx=pad, pady=pad, sticky=W)
        seats_sold_label.grid(row=3, column=1, padx=pad, pady=pad, sticky=E)

        labels['booked_seats'].grid(row=4, column=0, padx=pad, pady=pad, sticky=W)
        seats_booked_label.grid(row=4, column=1, padx=pad, pady=pad, sticky=E)

        labels['revenue'].grid(row=5, column=0, padx=pad, pady=pad, sticky=W)
        revenue_label.grid(row=5, column=1, padx=pad, pady=pad, sticky=E)


    def back(self):
        self.controller.show_frame('EventsPage')

    def sell(self):
        pass

    def book(self):
        pass

    def set_event(self, event):
        self.event = event

    def set_projection_room(self, projection_room):
        self.projection_room = projection_room

    def set_inputs(self):
        # day-month-year begin_hour - end_hour
        date = self.event['begin'].strftime("%d-%m-%Y %H")
        date += 'h - '
        date += (self.event['begin'] + timedelta(minutes=self.event['running_time'])).strftime("%H")
        date += 'h'
        seats_left = self.projection_room['total_seats'] - self.event['booked_seats'] - self.event['sold_seats']

        self.textvar['name'].set(self.event['name'])
        self.textvar['projection_type'].set(self.event['projection_type'])
        self.textvar['date'].set(date)
        self.textvar['seats_left'].set(seats_left)
        self.textvar['sold_seats'].set(self.event['sold_seats'])
        self.textvar['booked_seats'].set(self.event['booked_seats'])
        self.textvar['revenue'].set(self.event['revenue'])

