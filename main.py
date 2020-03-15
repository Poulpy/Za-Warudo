from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedTk
from ttkthemes import ThemedStyle

class App(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        # self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        # container = ttk.Frame(self)
        container = ttk.Frame(self)
        style = ThemedStyle(self)
        style.set_theme("arc")
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(ttk.Frame):

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        label = ttk.Label(self, text="This is the start page")#, font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        button1 = ttk.Button(self, text="Go to Page One",
                            command=lambda: controller.show_frame("PageOne"))
        button2 = ttk.Button(self, text="Go to Page Two",
                            command=lambda: controller.show_frame("PageTwo"))
        button1.pack()
        button2.pack()


class PageOne(ttk.Frame):

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        label = ttk.Label(self, text="This is page 1")#, font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = ttk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()


class PageTwo(ttk.Frame):

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        label = ttk.Label(self, text="This is page 2")#, font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = ttk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()


if __name__ == "__main__":
    app = App()
    app.mainloop()
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
        label.bind("<Button-1>", self.show)
        label.grid(row=1, column=1)

        self.entry = ttk.Entry(self)
        self.entry.grid(row=3, column=3)
        ttk.Button(self, text="Login", command=self.login).grid(row=3, column=4)

    def login(self):
        print("Login %s" % (self.entry.get()))

    def show(self, event):
        (parent.frames["EventsPage"]).tkraise()


class EventsPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = ttk.Label(self, text="Events")
        label.bind("<Button-1>", clickb)
        label.grid(row=1, column=1)


"""
window = ThemedTk(theme="arc")
window.frames = {}
window.geometry("500x500")

container = ttk.Frame(window)
container.grid(row=0, column=0)

events_page = EventsPage(window, container)
events_page.grid(row=0, column=0, sticky="nsew")
login_page = LoginPage(window, container)
login_page.grid(row=0, column=0, sticky="nsew")
window.frames["LoginPage"] = login_page
window.frames["EventsPage"] = events_page
(window.frames["LoginPage"]).tkraise()


window.mainloop()
"""
