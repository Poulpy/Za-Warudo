import logging as log
from tkinter import *
from tkinter import ttk

class ConnectionPage(ttk.Frame):
    '''
    Frame for the user to log in
    '''

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        pad = 10

        up = ttk.Frame(self, padding=(5, 5, 5, 5))
        down = ttk.Frame(self)

        self.notification_text = StringVar()

        connection_label = ttk.Label(up, text="Connection", font=("TkDefaultFont", "15"))

        # It's the input for the user's login
        self.login_entry = ttk.Entry(up)
        self.login_entry.focus()

        # It's the input for the user's password
        # The password is hidden with *
        self.password_entry = ttk.Entry(up, show="•")
        self.password_entry.bind("<Return>", self.login)

        login_button = ttk.Button(up, text="Login", command=self.login)

        # Label that shows if the authentification has failed
        notification_label = ttk.Label(down, textvariable=self.notification_text, justify=CENTER)
        notification_label.configure(style='Red.TLabel')

        up.grid_rowconfigure(0, weight=1)
        up.grid_rowconfigure(4, weight=1)
        up.grid_columnconfigure(0, weight=1)
        up.grid_columnconfigure(4, weight=1)

        connection_label.grid(row=0, column=1, sticky=N+S)
        notification_label.grid(row=0, column=1, padx=pad, pady=pad, sticky=NSEW)

        self.login_entry.grid(row=1, column=1, padx=pad, pady=pad, sticky=NSEW)

        self.password_entry.grid(row=2, column=1, padx=pad, pady=pad, sticky=NSEW)

        login_button.grid(row=3, column=1, padx=pad, pady=pad, sticky=N+S)

        up.place(rely=.4, relx=.5, anchor=CENTER)
        down.place(rely=.6, relx=.5, anchor=CENTER)

    def display_notification(self, message: str):
        '''
        Display something bellow the login button
        the color argument is a string denoting a style, ie, Red.TLabel, TEntry
        '''
        self.notification_text.set(message)
        log.info(message)


    def login(self, event=None):
        # We get the user input : login and password
        login = self.login_entry.get()
        password = self.password_entry.get()
        notif = self.controller.check_credentials(login, password)
        self.display_notification(notif)

