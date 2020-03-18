from tkinter import *
from tkinter import ttk
from tkcalendar import Calendar, DateEntry
from datetime import datetime

class EventsPage(ttk.Frame):

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        title = ttk.Label(self, text="Events")#, font=controller.title_font)
        #label.pack(side="top", fill="x", pady=10)
        log_out_button = ttk.Button(self, text="Log out",
                           command=lambda: controller.show_frame("ConnectionPage"))

        new_event_button = ttk.Button(self, text="New event")
        new_vacation_button = ttk.Button(self, text="New Vacation")
        timetable_button = ttk.Button(self, text="Timetable")

        date_button = ttk.Button(self, text='Choose date', command=self.choose_date)
        self.date_text = StringVar()
        self.date_label = ttk.Label(self, textvariable=self.date_text)
        self.date_text.set(datetime.now().strftime("%Y-%m-%d"))

        title.grid(row=0, column=0)
        timetable_button.grid(row=0, column=1)
        new_vacation_button.grid(row=0, column=2)
        new_event_button.grid(row=0, column=3)
        log_out_button.grid(row=0, column=4)

        date_button.grid(row=1, column=0)
        self.date_label.grid(row=1, column=1)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=2)

    def choose_date(self):
        def print_sel():
            print(cal.selection_get())

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

