from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedStyle
from gui.connection_page import ConnectionPage
from gui.events_page import EventsPage

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
        self.geometry("600x600")
        self.minsize(300, 300)
        self.title("ZA WARUDO")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (ConnectionPage, EventsPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)

        self.show_frame("ConnectionPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

