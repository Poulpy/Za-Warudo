from tkinter import *
from tkinter import ttk

class ConnectionPage(ttk.Frame):

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        connection_label = ttk.Label(self, text="Connection")
        connection_label.grid(row=0, column=1, sticky=S)


        self.login_entry = ttk.Entry(self)
        self.login_entry.grid(row=1, column=1, padx=5, pady=5, sticky=NSEW)

        self.password_entry = ttk.Entry(self)
        self.password_entry.grid(row=2, column=1, padx=5, pady=5, sticky=NSEW)

        login_button = ttk.Button(self, text="Login", command=lambda: controller.show_frame("EventsPage"))
        login_button.grid(row=3, column=1, padx=5, pady=5, sticky=N)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(4, weight=1)

