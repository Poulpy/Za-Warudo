from functools import partial
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
        # Event when the input has focus
        self.bind('<FocusIn>', self.choose_date)
        self.textvariable = kwargs['textvariable']
        self.parent = args[0]

    def choose_date(self, event=None):
        '''
        A calendar appears out of nowhere
        Click on the OK button to make it
        disappear... out of nowhere
        '''

        top = Toplevel(self.parent)

        cal = Calendar(top,
                       selectmode='day',
                       cursor="hand1",
                       locale="fr_FR",
                       date_pattern="y-mm-dd")
        cal.pack()
        #cal.pack(fill="both", expand=True)
        ttk.Button(top, text="OK", command=partial(self.get_calendar_input, top, cal)).pack()

    def get_calendar_input(self, top, cal):
        self.textvariable.set(cal.selection_get())
        top.destroy()
        self.parent.focus()

class Spinbox(ttk.Entry):

    def __init__(self, master=None, **kw):

        ttk.Entry.__init__(self, master, 'ttk::spinbox', **kw)


