from tkinter import *
from tkinter import ttk
from tkcalendar import Calendar, DateEntry
from datetime import datetime
import logging as log

class EditEventPage(ttk.Frame):

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller


        title = ttk.Label(self, text="Create event", font=("TkDefaultFont", "15"))
        back_button = ttk.Button(self, text='Back', command=lambda: self.controller.show_frame("EventsPage"))

        self.name_entry = ttk.Entry(self)
        begin_button = ttk.Button(self, text='Choose begin date', command=lambda: self.choose_date(self.set_begin_label))
        self.begin_text = StringVar()
        self.begin_label = ttk.Label(self, textvariable=self.begin_text)
        end_button = ttk.Button(self, text='Choose end date', command=lambda: self.choose_date(self.set_end_label))
        self.end_text = StringVar()
        self.end_label = ttk.Label(self, textvariable=self.end_text)

        title.grid(row=0, column=0, sticky=(W+N))
        back_button.grid(row=0, column=2, sticky=E)


    def set_begin_label(self):
        self.begin_text.set(cal.selection_get())

    def set_end_label(self):
        self.end_text.set(cal.selection_get())

    def choose_date(self, event):
        top = Toplevel(self)

        cal = Calendar(top,
                       selectmode='day',
                       cursor="hand1",
                       locale="fr_FR",
                       date_pattern="y-mm-dd")
        cal.pack(fill="both", expand=True)
        ttk.Button(top, text="OK", command=event).pack()


