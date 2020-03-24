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

        up = ttk.Frame(self, padding=(5, 5, 5, 5))
        down = ttk.Frame(self)

        connection_label = ttk.Label(up, text="Connection", font=("TkDefaultFont", "15"))
        connection_label.grid(row=0, column=1, sticky=S)

        # It's the input for the user's login
        self.login_entry = ttk.Entry(up)
        self.login_entry.grid(row=1, column=1, padx=5, pady=5, sticky=NSEW)
        self.login_entry.focus()

        # It's the input for the user's password
        # The password is hidden with *
        self.password_entry = ttk.Entry(up, show="•")
        self.password_entry.grid(row=2, column=1, padx=5, pady=5, sticky=NSEW)
        self.password_entry.bind("<Return>", self.controller.check_credentials)

        login_button = ttk.Button(up, text="Login", command=self.controller.check_credentials)
        login_button.grid(row=3, column=1, padx=5, pady=5, sticky=N)

        # Label that shows if the authentification has failed
        # TODO rename that var to fail_auth_label
        self.success_label_text = StringVar()
        self.success_label = ttk.Label(down, textvariable=self.success_label_text, justify=CENTER)
        self.success_label.grid(row=0, column=1, padx=5, pady=5, sticky=EW)

        # We place the components in the grid
        up.grid_rowconfigure(0, weight=1)
        up.grid_rowconfigure(4, weight=1)
        up.grid_columnconfigure(0, weight=1)
        up.grid_columnconfigure(4, weight=1)

        up.place(rely=.4, relx=.5, anchor=CENTER)
        down.place(rely=.6, relx=.5, anchor=CENTER)

    def display_notification(self, message: str, color: str):
        '''
        Display something bellow the login button
        the color argument is a string denoting a style, ie, Red.TLabel, TEntry
        '''
        self.success_label_text.set(message)
        self.success_label.configure(style=color)
        log.info(message)

