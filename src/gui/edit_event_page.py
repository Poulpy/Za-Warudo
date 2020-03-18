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

        name_label = ttk.Label(self, text="Name")
        self.name_entry = ttk.Entry(self)

        self.begin_text = StringVar()
        self.end_text = StringVar()
        begin = ttk.Label(self, text="Begin date")
        self.begin_entry = ttk.Entry(self, textvariable=self.begin_text)
        self.begin_entry.bind('<1>', self.choose_begin_date)
        end = ttk.Label(self, text="End date")
        self.end_entry = ttk.Entry(self, textvariable=self.end_text)
        self.end_entry.bind('<1>', self.choose_end_date)


        title.grid(row=0, column=0, sticky=(W+N))
        back_button.grid(row=0, column=2, sticky=E)

        name_label.grid(row=1, column=0)
        self.name_entry.grid(row=1, column=1)

        begin.grid(row=2, column=0)
        self.begin_entry.grid(row=2, column=1)
        end.grid(row=3, column=0)
        self.end_entry.grid(row=3, column=1)


    def set_begin_label(self, txt, event=None):
        print("begin " + txt.strftime("%Y-%m-%d %H:%M"))
        self.begin_text.set(txt)

    def set_end_label(self, txt, event=None):
        print("end " + txt.strftime("%Y-%m-%d %H:%M"))
        self.end_text.set(txt)

    def choose_begin_date(self, event=None):
        self.choose_date(self.set_begin_label)

    def choose_end_date(self, event=None):
        self.choose_date(self.set_end_label)

    def choose_date(self, event):
        top = Toplevel(self)

        cal = Calendar(top,
                       selectmode='day',
                       cursor="hand1",
                       locale="fr_FR",
                       date_pattern="y-mm-dd")
        cal.pack(fill="both", expand=True)
        ttk.Button(top, text="OK", command=combine_funcs(lambda: event(cal.selection_get()), lambda: top.destroy())).pack()



def combine_funcs(*funcs):
    def combined_func(*args, **kwargs):
        for f in funcs:
            f(*args, **kwargs)
    return combined_func

