import logging as log
from tkinter import *
from tkinter import ttk

class TicketingPage(ttk.Frame):
    '''
    Page to book or sell tickets
    '''

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        self.textvar = dict()
        for var in ('seats_left', 'seats_sold', 'seats_booked', 'revenue'):
            self.textvar[var] = StringVar()

        tickets_frame = ttk.Frame(self)

        back_button = ttk.Button(self, text='Back', command=lambda: self.back())
        sell_button = ttk.Button(self, text='Sell', command=lambda: self.sell())
        book_button = ttk.Button(self, text='Book', command=lambda: self.book())

        event_name_label = ttk.Label(self, text='')
        event_date_label = ttk.Label(self, text='')
        seats_left_label = ttk.Label(self, textvariable=self.textvar['seats_left'])
        seats_sold_label = ttk.Label(self, textvariable=self.textvar['seats_sold'])
        seats_booked_label = ttk.Label(self, textvariable=self.textvar['seats_booked'])
        revenue_label = ttk.Label(self, textvariable=self.textvar['revenue'])

    def back(self):
        pass

    def sell(self):
        pass

    def book(self):
        pass

