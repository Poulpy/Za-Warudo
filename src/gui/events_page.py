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
        new_event_button.grid(row=0, column=1, sticky=(W+E))

        self.date_text = StringVar()
        self.date_entry = EntryDate(self, textvariable=self.date_text)
        self.date_label = ttk.Label(self, textvariable=self.date_text)
        self.date_text.set(datetime.now().strftime("%Y-%m-%d"))

        self.date_entry.grid(row=1, column=1, sticky=(W+E))
        ttk.Button(self, text="Edit").grid(row=2, column=1, sticky=(W+E))
        ttk.Button(self, text="Details").grid(row=3, column=1, sticky=(W+E))
        ttk.Button(self, text="Delete").grid(row=4, column=1, sticky=(W+E))
        ttk.Button(self, text="Ticketing").grid(row=5, column=1, sticky=(W+E))


        # self.date_label.grid(row=1, column=2, sticky=W)

        self.grid_columnconfigure(0, weight=2)


        events = self.controller.get_events(self.date_text.get())
        events_box = Listbox(self)
        for i, event in enumerate(events.dicts()):
            events_box.insert(END, event['name'] + " " + event['begin'].strftime("%H:%M") + '-' + event['end'].strftime("%H:%M"))

        events_box.grid(column=0, row=1, rowspan=5, sticky=NSEW)


    def display_events(self, top, cal):
        #top.destroy()
        #self.date_text.set(cal.selection_get())
        log.info(self.controller.get_events(self.date_text.get()))

    def set_displayed_events(self):
        self.frames = [None for i in range(events.count())]
        for i, event in enumerate(events.dicts()):
            self.frames[i] = ttk.Frame(self)
            ttk.Label(self.frames[i], text=event['name']).grid(row=0, column=0, sticky=W)
            date = event['begin'].strftime("%H:%M") + '-' + event['end'].strftime("%H:%M")
            ttk.Label(self.frames[i], text=date).grid(row=1, column=0)
            ttk.Button(self.frames[i], text="Edit").grid(row=0, column=2, sticky=E)
            ttk.Button(self.frames[i], text="Details").grid(row=1, column=2, sticky=E)
            ttk.Button(self.frames[i], text="Delete").grid(row=2, column=2, sticky=E)
            ttk.Button(self.frames[i], text="Ticketing").grid(row=3, column=2, sticky=E)
            self.frames[i].grid_columnconfigure(0, weight=2)
            self.frames[i].grid_columnconfigure(1, weight=2)
            self.frames[i].pack(side=LEFT)
            #self.frames[i].grid(row=0, column=0)

