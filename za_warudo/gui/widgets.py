from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedStyle
from tkcalendar import Calendar, DateEntry

class EntryDate(ttk.Entry):
    '''
    Entry for selecting a date
    '''

    def __init__(self, *args, **kwargs):
        if not "textvariable" in kwargs.keys(): raise ArgumentError("Must take textvariable")
        ttk.Entry.__init__(self, *args, **kwargs)
        # TODO change the bind to 'focus' instead of clicking
        # because the user might do a tab and then get the
        # focus, but not clicking
        self.bind('<1>', self.choose_date)
        self.textvariable = kwargs['textvariable']

    def choose_date(self, event=None):
        '''
        A calendar appears out of nowhere
        Click on the OK button to make it
        disappear... out of nowhere
        '''

        top = Toplevel(self)

        cal = Calendar(top,
                       selectmode='day',
                       cursor="hand1",
                       locale="fr_FR",
                       date_pattern="y-mm-dd")
        cal.pack(fill="both", expand=True)
        ttk.Button(top, text="OK", command=combine_funcs(lambda: self.textvariable.set(cal.selection_get()), lambda: top.destroy())).pack()

class Spinbox(ttk.Entry):

    def __init__(self, master=None, **kw):

        ttk.Entry.__init__(self, master, 'ttk::spinbox', **kw)


def combine_funcs(*funcs):
    def combined_func(*args, **kwargs):
        for f in funcs:
            f(*args, **kwargs)
    return combined_func

