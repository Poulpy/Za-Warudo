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

        # Grid
        back_button.grid(row=0, column=4, padx=pad, pady=pad)

        label['name'].grid(row=1, column=0, padx=pad, pady=pad, sticky=W)
        value['name'].grid(row=1, column=1, padx=pad, pady=pad, sticky=E)
        label['seats_left'].grid(row=1, column=2, padx=pad, pady=pad, sticky=W)
        value['seats_left'].grid(row=1, column=3, padx=pad, pady=pad, sticky=W)

        label['projection_type'].grid(row=2, column=0, padx=pad, pady=pad, sticky=W)
        value['projection_type'].grid(row=2, column=1, padx=pad, pady=pad, sticky=E)
        label['sold_seats'].grid(row=2, column=2, padx=pad, pady=pad, sticky=W)
        value['sold_seats'].grid(row=2, column=3, padx=pad, pady=pad, sticky=W)

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


    def timetable(self):
        pass

    def back(self):
        self.controller.show_frame('EventsPage')

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


