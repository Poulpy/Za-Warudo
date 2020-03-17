from tkinter import *
from tkinter import ttk
from tkcalendar import Calendar, DateEntry

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

        title.grid(row=0, column=0)
        timetable_button.grid(row=0, column=1)
        new_vacation_button.grid(row=0, column=2)
        new_event_button.grid(row=0, column=3)
        log_out_button.grid(row=0, column=4)

        self.grid_columnconfigure(0, weight=2)
        ttk.Button(self, text='Calendar', command=self.example1).grid(row=1, column=0)
        ttk.Button(self, text='DateEntry', command=self.example2).grid(row=1, column=1)

    def example1(self):
        def print_sel():
            print(cal.selection_get())

        top = Toplevel(self)

        cal = Calendar(top,
                       font="Arial 14", selectmode='day',
                       cursor="hand1", year=2018, month=2, day=5)
        cal.pack(fill="both", expand=True)
        ttk.Button(top, text="ok", command=print_sel).pack()

    def example2(self):
        top = Toplevel(self)

        ttk.Label(top, text='Choose date').pack(padx=10, pady=10)

        cal = DateEntry(top, width=12, background='darkblue',
                        foreground='white', borderwidth=2)
        cal.pack(padx=10, pady=10)
