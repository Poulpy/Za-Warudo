from tkinter import ttk
from tkinter import LEFT, RIGHT
from tkinter import W
from ttkthemes import ThemedTk

def hello():
    print("Hello")

def clickb(event):
    print("there's a click!")


class LoginPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ttk.Button(self, text="Hello", command=hello).grid(row=1)
        label = ttk.Label(self, text="Connection")
        label.bind("<Button-1>", clickb)
        label.grid(row=1, column=1)

        self.entry = ttk.Entry(self)
        self.entry.grid(row=3, column=3)
        ttk.Button(self, text="Login", command=self.login).grid(row=3, column=4)

    def login(self):
        print("Login %s" % (self.entry.get()))

window = ThemedTk(theme="arc")
window.frames = {}
window.geometry("500x500")

container = ttk.Frame(window)
container.grid(row=0, column=0)

login_page = LoginPage(window, container)
login_page.grid(row=0, column=0)
window.frames["LoginPage"] = login_page
(window.frames["LoginPage"]).tkraise()
window.mainloop()

