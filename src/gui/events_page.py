from tkinter import *
from tkinter import ttk
from tkcalendar import Calendar, DateEntry
from datetime import datetime
import logging as log

class EventsPage(ttk.Frame):

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        header = ttk.Frame(self)
        body = ttk.Frame(self)

        title = ttk.Label(header, text="Events", font=("TkDefaultFont", "20"))#, font=controller.title_font)
        #label.pack(side="top", fill="x", pady=10)
        log_out_button = ttk.Button(header, text="Log out",
                           command=lambda: controller.show_frame("ConnectionPage"))

        new_event_button = ttk.Button(header, text="New event")

        title.grid(row=0, column=0, sticky=(W+N))
        new_event_button.grid(row=0, column=2, sticky=E)

        date_button = ttk.Button(header, text='Choose date', command=self.choose_date)
        self.date_text = StringVar()
        self.date_label = ttk.Label(header, textvariable=self.date_text)
        self.date_text.set(datetime.now().strftime("%Y-%m-%d"))
        events = self.controller.get_events(self.date_text.get())


        date_button.grid(row=1, column=0, sticky=W)
        self.date_label.grid(row=1, column=2, sticky=W)

        header.grid_columnconfigure(1, weight=2)

        header.pack(side=TOP, expand=True, fill='both')
        # header.grid(row=0, column=0)

        frames = [None for i in range(events.count())]
        for i, event in enumerate(events.dicts()):
            frames[i] = ttk.Frame(body)
            ttk.Label(frames[i], text=event['name']).grid(row=0, column=0, sticky=W)
            ttk.Button(frames[i], text="Edit").grid(row=0, column=2, sticky=E)
            ttk.Button(frames[i], text="Details").grid(row=1, column=2, sticky=E)
            ttk.Button(frames[i], text="Delete").grid(row=2, column=2, sticky=E)
            ttk.Button(frames[i], text="Ticketing").grid(row=3, column=2, sticky=E)
            frames[i].grid_columnconfigure(0, weight=2)
            frames[i].grid_columnconfigure(1, weight=2)
            frames[i].pack(side=LEFT)
            #frames[i].grid(row=0, column=0)

        body.pack(side=TOP, expand=True, fill='both')
        # body.grid(row=1, column=0)


    def choose_date(self):
        top = Toplevel(self)

        cal = Calendar(top,
                       selectmode='day',
                       cursor="hand1",
                       locale="fr_FR",
                       date_pattern="y-mm-dd")
        cal.pack(fill="both", expand=True)
        ttk.Button(top, text="OK", command=lambda: self.display_events(top, cal)).pack()

    def display_events(self, top, cal):
        top.destroy()
        self.date_text.set(cal.selection_get())
        log.info(self.controller.get_events(self.date_text.get()))

    def example2(self):
        top = Toplevel(self)

        ttk.Label(top, text='Choose date').pack(padx=10, pady=10)

        cal = DateEntry(top, width=12, background='darkblue',
                        foreground='white', borderwidth=2)
        cal.pack(padx=10, pady=10)

    def example3(self):

        top = Toplevel(self)

        cal = Calendar(top, selectmode='none')
        date = cal.datetime.today() + cal.timedelta(days=2)
        cal.calevent_create(date, 'Hello World', 'message')
        cal.calevent_create(date, 'Reminder 2', 'reminder')
        cal.calevent_create(date + cal.timedelta(days=-2), 'Reminder 1', 'reminder')
        cal.calevent_create(date + cal.timedelta(days=3), 'Message', 'message')

        cal.tag_config('reminder', background='red', foreground='yellow')

        cal.pack(fill="both", expand=True)
        ttk.Label(top, text="Hover over the events.").pack()

