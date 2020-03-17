from tkinter import *
from tkinter import ttk
from peewee import *
from user import User
import logging as log

db = SqliteDatabase("db/app.db")

class ConnectionPage(ttk.Frame):

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        up = ttk.Frame(self, padding=(5, 5, 5, 5))
        down = ttk.Frame(self)

        connection_label = ttk.Label(up, text="Connection")
        connection_label.grid(row=0, column=1, sticky=S)

        self.login_entry = ttk.Entry(up)
        self.login_entry.grid(row=1, column=1, padx=5, pady=5, sticky=NSEW)

        self.password_entry = ttk.Entry(up, show="*")
        self.password_entry.grid(row=2, column=1, padx=5, pady=5, sticky=NSEW)

        login_button = ttk.Button(up, text="Login", command=self.check_credentials)
        login_button.grid(row=3, column=1, padx=5, pady=5, sticky=N)

        self.success_label_text = StringVar()
        self.success_label = ttk.Label(down, textvariable=self.success_label_text, justify=CENTER)
        self.success_label.grid(row=0, column=1, padx=5, pady=5, sticky=EW)

        up.grid_rowconfigure(0, weight=1)
        up.grid_rowconfigure(4, weight=1)
        up.grid_columnconfigure(0, weight=1)
        up.grid_columnconfigure(4, weight=1)

        up.place(rely=.4, relx=.5, anchor=CENTER)
        down.place(rely=.65, relx=.5, anchor=CENTER)

    def display_notification(self, message: str, color: str):
        self.success_label_text.set(message)
        self.success_label.configure(style=color)
        log.info(message)


    def check_credentials(self):
        self.s = ttk.Style()
        self.s.configure("Red.TLabel", foreground="red")
        # self.s.configure("Green.TLabel", foreground="green")

        db.connect()
        login = self.login_entry.get()
        password = self.password_entry.get()

        u = User.select().where(User.login == login).first()

        if u == None:
            self.success_label_text.set("Authentification failed : no user found")
            self.success_label.configure(style="Red.TLabel")
            log.info("Authentification failed : no user found")
        else:
            if password == u.password:
                log.info("Authentification successfull")
                self.controller.show_frame("EventsPage")
            else:
                self.success_label_text.set("Authentification failed : password incorrect")
                self.success_label.configure(style="Red.TLabel")
                log.info("Authentification failed : password incorrect")

        db.close()

