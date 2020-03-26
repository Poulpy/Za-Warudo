from functools import partial
from datetime import datetime
from datetime import timedelta
from tkinter import *
from tkinter import ttk
import logging as log

from gui.widgets import Spinbox

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

        for var in ('name', 'projection_type', 'location', 'date', 'seats_left', 'sold_seats', 'booked_seats', 'revenue'):
            self.textvar[var] = StringVar()
            labels[var] = ttk.Label(self, text=var.capitalize().replace('_', ' '))

        self.tickets_frame = ttk.Frame(self)

        # Buttons
        back_button = ttk.Button(self, text='Back', command=self.back)
        sell_button = ttk.Button(self, text='Sell', command=partial(self.pass_order, 'sell'))
        book_button = ttk.Button(self, text='Book', command=partial(self.pass_order, 'book'))

        # Labels
        event_name_label = ttk.Label(self, textvariable=self.textvar['name'], font=("TkDefaultFont", "15"))
        event_type_label = ttk.Label(self, textvariable=self.textvar['projection_type'])
        location_label = ttk.Label(self, textvariable=self.textvar['location'])
        event_date_label = ttk.Label(self, textvariable=self.textvar['date'])
        seats_left_label = ttk.Label(self, textvariable=self.textvar['seats_left'])
        seats_sold_label = ttk.Label(self, textvariable=self.textvar['sold_seats'])
        seats_booked_label = ttk.Label(self, textvariable=self.textvar['booked_seats'])
        revenue_label = ttk.Label(self, textvariable=self.textvar['revenue'])


        # GRID
        event_name_label.grid(row=0, column=0, padx=pad, pady=pad)
        event_type_label.grid(row=0, column=1, padx=pad, pady=pad)
        location_label.grid(row=0, column=2, padx=pad, pady=pad)
        back_button.grid(row=0, column=4, padx=pad, pady=pad)

        event_date_label.grid(row=1, column=1, padx=pad, pady=pad, sticky=E)
        self.tickets_frame.grid(row=1, column=2, rowspan=5, padx=pad, pady=pad, sticky=NSEW)

        labels['seats_left'].grid(row=2, column=0, padx=pad, pady=pad, sticky=W)
        seats_left_label.grid(row=2, column=1, padx=pad, pady=pad, sticky=E)

        labels['sold_seats'].grid(row=3, column=0, padx=pad, pady=pad, sticky=W)
        seats_sold_label.grid(row=3, column=1, padx=pad, pady=pad, sticky=E)

        labels['booked_seats'].grid(row=4, column=0, padx=pad, pady=pad, sticky=W)
        seats_booked_label.grid(row=4, column=1, padx=pad, pady=pad, sticky=E)

        labels['revenue'].grid(row=5, column=0, padx=pad, pady=pad, sticky=W)
        revenue_label.grid(row=5, column=1, padx=pad, pady=pad, sticky=E)

        sell_button.grid(row=6, column=0, padx=pad, pady=pad, sticky=NSEW)
        book_button.grid(row=6, column=1, padx=pad, pady=pad, sticky=NSEW)


    def get_seats(self) -> int:
        '''
        Return the number of seats requested
        '''
        seats = 0

        for s in self.seats:
            if s['var'].get() != '':
                seats += int(s['var'].get())

        return seats

    def total_price(self) -> int:
        '''
        Return the total price, given a price and the number
        of seats
        '''
        total = 0

        for s in self.seats:
            if s['var'].get() != '':
                total += s['price'] * int(s['var'].get())

        return total

    def back(self):
        '''
        Go back to the events page and update the events displayed
        '''
        self.controller.show_frame('EventsPage')
        self.controller.update_events_page()

    def pass_order(self, order_type):
        '''
        Sell or book seats for the event
        '''
        values_to_update = dict()
        if order_type == 'sell':
            values_to_update['sold_seats'] = self.event.sold_seats + self.get_seats()
        elif order_type == 'book':
            values_to_update['booked_seats'] = self.event.booked_seats + self.get_seats()
        else:
            return

        values_to_update['revenue'] = self.event.revenue + self.total_price()

        if values_to_update['revenue'] == 0:
            log.info('No revenue : no seats sold or booked ?')
            return

        log.info(values_to_update)
        self.controller.update(self.event.id, values_to_update)
        self.event = self.controller.get_event_by_id(self.event.id)
        self.display_events_seats_information()

    def set_event(self, event):
        self.event = event

    def set_projection_room(self, projection_room):
        self.projection_room = projection_room

    def display_events_seats_information(self):
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
        self.textvar['revenue'].set(revenue)

    def set_inputs(self):
        pad = 5
        self.display_events_seats_information()

        for widget in self.tickets_frame.winfo_children():
            widget.destroy()

        categories = self.controller.get_categories_for_event(self.event)
        log.debug(categories)
        self.seats = [None for i in categories]
        for i, c in enumerate(categories):
            self.seats[i] = {'price':c.price, 'var':StringVar()}
            price = str(c.price) + ' €'

            ttk.Label(self.tickets_frame, text=c.title).grid(row=i, column=0, padx=pad, pady=pad, sticky=W)
            ttk.Label(self.tickets_frame, text=price).grid(row=i, column=1, padx=pad, pady=pad, sticky=W)
            Spinbox(self.tickets_frame, textvariable=self.seats[i]['var'], from_=0, to=90).grid(row=i, column=2, padx=pad, pady=pad, sticky=E)
            self.seats[i]['var'].set(0)

