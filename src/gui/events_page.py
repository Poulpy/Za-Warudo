from tkinter import *
from tkinter import ttk

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
