from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedStyle
from tkcalendar import Calendar, DateEntry

class EntryDate(ttk.Entry):

    def __init__(self, *args, **kwargs):
        if not "textvariable" in kwargs.keys(): raise ArgumentError("Must take textvariable")
        ttk.Entry.__init__(self, *args, **kwargs)
        self.bind('<1>', self.choose_date)
        self.textvariable = kwargs['textvariable']

    def choose_date(self, event=None):
        top = Toplevel(self)

        cal = Calendar(top,
                       selectmode='day',
                       cursor="hand1",
                       locale="fr_FR",
                       date_pattern="y-mm-dd")
        cal.pack(fill="both", expand=True)
        ttk.Button(top, text="OK", command=combine_funcs(lambda: self.textvariable.set(cal.selection_get()), lambda: top.destroy())).pack()

def combine_funcs(*funcs):
    def combined_func(*args, **kwargs):
        for f in funcs:
            f(*args, **kwargs)
    return combined_func

