from functools import partial
from datetime import datetime
from datetime import timedelta
from tkinter import *
from tkinter import ttk
import logging as log

from tkcalendar import Calendar, DateEntry

from gui.widgets import EntryDate

class NewVacationPage(ttk.Frame):

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        self.parent = parent
        pad = 5

        labels = dict()
        entries = dict()
        self.textvar = dict()

        self.textvar['notification'] = StringVar()
        labels['notification'] = ttk.Label(self, textvariable=self.textvar['notification'])
        labels['title'] = ttk.Label(self, text='New vacation', font=("TkDefaultFont", "15"))

        for f in ('begin', 'end', 'reason'):
            labels[f] = ttk.Label(self, text=f.capitalize())
            self.textvar[f] = StringVar()

        save_button = ttk.Button(self, text='Save', command=self.save)


        entries['begin'] = EntryDate(self, textvariable=self.textvar['begin'])
        entries['end'] = EntryDate(self, textvariable=self.textvar['end'])
        entries['reason'] = ttk.Entry(self, textvariable=self.textvar['reason'])

        labels['title'].grid(row=0, column=0, padx=pad, pady=pad, sticky=W)
        save_button.grid(row=0, column=3)

        labels['begin'].grid(row=1, column=0, padx=pad, pady=pad, sticky=W)
        entries['begin'].grid(row=1, column=1, padx=pad, pady=pad, sticky=E)

        labels['end'].grid(row=2, column=0, padx=pad, pady=pad, sticky=W)
        entries['end'].grid(row=2, column=1, padx=pad, pady=pad, sticky=E)

        labels['reason'].grid(row=3, column=0, padx=pad, pady=pad, sticky=W)
        entries['reason'].grid(row=3, column=1, padx=pad, pady=pad, sticky=E)

        labels['notification'].grid(row=4, column=0, columnspan=3, padx=pad, pady=pad, sticky=W)

    def save(self):
        new_vacation = dict()

        new_vacation['begin'] = datetime.strptime(self.textvar['begin'].get(), "%Y-%m-%d")
        new_vacation['end'] = datetime.strptime(self.textvar['end'].get(), "%Y-%m-%d")
        new_vacation['reason'] = self.textvar['reason'].get()

        if new_vacation['begin'] > new_vacation['end']:
            self.textvar['notification'].set("Begin date can't be superior to end date")
            return

        log.info(new_vacation)
        self.controller.new_vacation(new_vacation)
        self.parent.destroy()


