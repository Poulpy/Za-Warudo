from datetime import datetime
from tkinter import *
from tkinter import ttk
import logging as log
import re

import ttkwidgets as tkw
from tkcalendar import Calendar, DateEntry

from gui.entry_date import EntryDate

class EditEventPage(ttk.Frame):
    '''
    Frame to create a new event
    Upon creation the user is redirected to the events page
    TODO frame to create AND edit an event
    '''

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        self.error_text = StringVar()
        title = ttk.Label(self, text="Create event", font=("TkDefaultFont", "15"))
        error_label = ttk.Label(self, textvariable=self.error_text, font=("TkDefaultFont", "7"))
        error_label.configure(style="Red.TLabel")
        buttons_frame = ttk.Frame(self)
        back_button = ttk.Button(buttons_frame, text='Back', command=lambda: self.controller.show_frame("EventsPage"))

        # And of course, the button to save it all
        save_button = ttk.Button(buttons_frame, text="Save", command=self.save)

        # Event form
        name_label = ttk.Label(self, text="Name")
        self.name_entry = ttk.Entry(self)

        # Variables to get the values after input
        self.begin_text = StringVar()
        self.hour_text = StringVar()
        self.running_time_text = StringVar()

        self.hour_text.set('12')
        self.running_time_text.set('60')

        # Input for the date of the event
        begin = ttk.Label(self, text="Day")
        begin_entry = EntryDate(self, textvariable=self.begin_text)
        # Input for the hour of the event
        hour = ttk.Label(self, text="Hour")
        hour_entry = Spinbox(self, from_=0, to=24, textvariable=self.hour_text)
        # Input for the running time, in minutes
        # TODO actually we can type anything in this s* widget
        # do something to prevent that by using regex
        # When clicking on the save button, there may be a label
        # if the input is wrong
        running_time = ttk.Label(self, text="Running time (minutes)")
        running_time_entry = Spinbox(self, from_=0, to=500, textvariable=self.running_time_text)

        # Dropdown list for the type of the projection (film, docu)
        pj_label = ttk.Label(self, text="Projection type")
        self.projection_type_choosen = StringVar()
        projection_types = ttk.Combobox(self, textvariable=self.projection_type_choosen, state='readonly')
        projection_types['values'] = ["Film", "Documentary"]
        projection_types.current(0)

        pjs = [pj['location'] for pj in controller.get_projection_rooms().dicts()]

        # Dropdown list for the location of the event
        pr_label = ttk.Label(self, text="Projection room")
        self.projection_room_choosen = StringVar()
        projection_rooms = ttk.Combobox(self, textvariable=self.projection_room_choosen, state='readonly')
        projection_rooms['values'] = pjs
        projection_rooms.current(0)

        # Inputs for the event's status to go 'finished'
        check_frame = ttk.Frame(self)
        room_chbutton = ttk.Checkbutton(check_frame, text="Room reserved")
        equipment_chbutton = ttk.Checkbutton(check_frame, text="Equipment reserved")
        management_chbutton = ttk.Checkbutton(check_frame, text="Management reserved")
        guest_attendance_chbutton = ttk.Checkbutton(check_frame, text="Guest attendance confirmed")


        # TODO the user can assign users to this event
        members_label = ttk.Label(self, text="Add members")
        user_names = [u['name'] for u in controller.get_users().dicts() if not u['is_admin']]

        members_frame = ttk.Frame(self)
        members_scrollbar = ttk.Scrollbar(members_frame, orient=VERTICAL)
        # List of users; the responsible has to choose among them
        # members that'll participate in the event's organisation
        self.members_tree = tkw.CheckboxTreeview(members_frame, columns=('Events'), selectmode='browse', yscrollcommand=members_scrollbar.set)
        members_scrollbar.configure(command=self.members_tree.yview)

        self.members_tree.column("Events")#, width=50)
        self.members_tree.heading("#0", text="Name")
        self.members_tree.heading("Events", text="Events")

        self.members_tree.tag_configure('odd', background="#F0F0F0")
        self.members_tree.tag_configure('even', background="#FAFAFA")
        for i, user in enumerate(user_names):
            self.members_tree.insert('', 'end', text=user, tags=('even' if i % 2 else 'odd',))

        # CATEGORIES
        categories_label = ttk.Label(self, text="Add categories")
        categories = controller.get_categories().dicts()

        cats_frame = ttk.Frame(self)
        cats_scrollbar = ttk.Scrollbar(cats_frame, orient=VERTICAL)
        self.cats_tree = tkw.CheckboxTreeview(cats_frame, columns=('Price'), selectmode='none')
        cats_scrollbar.configure(command=self.cats_tree.yview)
        self.cats_tree.column("#0", width=140)
        self.cats_tree.column("Price", anchor='center')
        self.cats_tree.heading("#0", text="Title")
        self.cats_tree.heading("Price", text="Price")

        self.cats_tree.tag_configure('odd', background="#F0F0F0")
        self.cats_tree.tag_configure('even', background="#FAFAFA")

        for i, category in enumerate(categories):
            s = '%d%s' % (category['price'], ' €')
            self.cats_tree.insert('', 'end', text=category['title'], tags=('even' if i % 2 else 'odd',), values=(s,))

        # PRESENTATION
        self.presentation = IntVar()
        self.author = StringVar()
        self.context = StringVar()

        presentation_frame = ttk.Frame(self)
        presentation_check = ttk.Checkbutton(presentation_frame,
                                             text="Author presentation",
                                             variable=self.presentation,
                                             command=lambda: self.handle_presentation_frame)
        presentation_check.bind('<1>', self.handle_presentation_frame)
        author_label = ttk.Label(presentation_frame, text="Author")
        self.author_entry = ttk.Entry(presentation_frame, textvariable=self.author, state='disabled')
        context_label = ttk.Label(presentation_frame, text="Context")
        self.context_entry = ttk.Entry(presentation_frame, textvariable=self.context, state='disabled')

        # DEBATE
        self.debate = IntVar()
        self.speaker = StringVar()
        self.contact_details = StringVar()

        debate_frame = ttk.Frame(self)
        debate_check = ttk.Checkbutton(debate_frame,
                                       text="Debate",
                                       variable=self.debate,
                                       command=lambda: self.handle_debate_frame)
        debate_check.bind('<1>', self.handle_debate_frame)
        speaker_label = ttk.Label(debate_frame, text="Speaker")
        self.speaker_entry = ttk.Entry(debate_frame, textvariable=self.speaker, state='disabled')
        contact_label = ttk.Label(debate_frame, text="Contact details")
        self.contact_entry = ttk.Entry(debate_frame, textvariable=self.contact_details, state='disabled')

        '''
        periodicity_label = ttk.Label(self, text="Periodicity")
        self.periodicity_choosen = StringVar()
        periodicities = ttk.Combobox(self,
                                     textvariable=self.periodicity_choosen,
                                     state='readonly',
                                     command=lambda: self.handle_periodicity_frame)
        periodicities['values'] = ["None", "One week", "Two weeks", "One month"]
        periodicities.current(0)
        week_end_check = ttk.Checkbutton(self, text="Weekend included", variable=self.week_ends)
        '''


        # Placing the components
        # ROW 0
        title.grid(row=0, column=0, sticky=(W+N))
        error_label.grid(row=0, column=1, sticky=W+N+S, columnspan=3, padx=(10, 0))
        buttons_frame.grid(row=0, column=5, sticky=E)
        back_button.grid(row=0, column=2, pady=5, padx=5, sticky=E)
        save_button.grid(row=0, column=3, pady=5, padx=5, sticky=E)

        # ROW 1
        name_label.grid(row=1, column=0, sticky=W, pady=5, padx=5)
        self.name_entry.grid(row=1, column=1, pady=5, padx=5, sticky=E)
        running_time.grid(row=1, column=2, pady=5, padx=5, sticky=W)
        running_time_entry.grid(row=1, column=3, pady=5, padx=5, sticky=E)

        # ROW 2
        begin.grid(row=2, column=0, sticky=W, pady=5, padx=5)
        begin_entry.grid(row=2, column=1, sticky=E, pady=5, padx=5)
        hour.grid(row=2, column=2, sticky=W, pady=5, padx=5)
        hour_entry.grid(row=2, column=3, sticky=E, pady=5, padx=5)

        # ROW 3

        # ROW 4
        pj_label.grid(row=3, column=0, sticky=W, pady=5, padx=5)
        projection_types.grid(row=3, column=1, sticky=E, pady=5, padx=5)
        pr_label.grid(row=3, column=2, pady=5, sticky=W, padx=5)
        projection_rooms.grid(row=3, column=3, sticky=E, pady=5, padx=5)

        # ROW 5
        # self.grid_rowconfigure(7, weight=3)
        presentation_frame.grid(row=1, column=4, sticky=NSEW, columnspan=2, rowspan=2, pady=5, padx=5)
        presentation_check.grid(row=0, column=0, sticky=W)
        author_label.grid(row=1, column=0, sticky=W, padx=(20, 0))
        self.author_entry.grid(row=1, column=1, sticky=E)
        context_label.grid(row=2, column=0, sticky=W, padx=(20, 0))
        self.context_entry.grid(row=2, column=1, sticky=E)


        debate_frame.grid(row=3, column=4, sticky=NSEW, rowspan=2, columnspan=2, pady=5, padx=5)
        debate_check.grid(row=0, column=0, sticky=W)
        speaker_label.grid(row=1, column=0, sticky=W, padx=(20, 0))
        self.speaker_entry.grid(row=1, column=1, sticky=E)
        contact_label.grid(row=2, column=0, sticky=W, padx=(20, 0))
        self.contact_entry.grid(row=2, column=1, sticky=E)

        check_frame.grid(row=5, column=4, rowspan=2, columnspan=2, sticky=N+W, pady=5, padx=5)
        room_chbutton.grid(row=4, column=2, sticky=W)
        equipment_chbutton.grid(row=5, column=2, sticky=W)
        management_chbutton.grid(row=6, column=2, sticky=W)
        guest_attendance_chbutton.grid(row=7, column=2, sticky=W)

        # ROW 6
        # self.grid_rowconfigure(6, weight=0)
        members_frame.grid(row=5, column=0, columnspan=2, pady=5, padx=5, sticky=NSEW)
        members_label.grid(row=4, column=0, pady=5, padx=5, sticky=W)
        # members_frame.pack_propagate(0)
        self.members_tree.pack(side=LEFT)
        members_scrollbar.pack()

        categories_label.grid(row=4, column=2, pady=5, padx=5, sticky=W)
        cats_frame.grid(row=5, column=2, columnspan=2, pady=5, padx=5, sticky=NSEW)
        self.cats_tree.pack(side=LEFT, expand=True)
        cats_scrollbar.pack()


    # 1 : unchecked
    # 0 : checked
    def handle_presentation_frame(self, event=None):
        print("Value of checkbox : " + str(self.presentation.get()))
        if self.presentation.get() == 1:
            self.author_entry['state'] = 'disabled'
            self.context_entry['state'] = 'disabled'
        else:
            self.author_entry['state'] = 'normal'
            self.context_entry['state'] = 'normal'

    def handle_debate_frame(self, event=None):
        print("Value of checkbox : " + str(self.debate.get()))
        if self.debate.get() == 1:
            self.speaker_entry['state'] = 'disabled'
            self.contact_entry['state'] = 'disabled'
        else:
            self.speaker_entry['state'] = 'normal'
            self.contact_entry['state'] = 'normal'

    def check_missing_or_incorrect_input(self):
        '''
        Name, day, hour, running time, must not be empty
        p = re.compile('^(2[0-4]|1[0-9]|[1-9])$')
        if p.match(self.hour_text.get()) == None:
            print("Wrong hour format")
        '''
        error_msg = []

        if self.name_entry.get() == '':
            error_msg.append('Name')
        if self.begin_text.get() == '':
            error_msg.append('Day')
        if self.hour_text.get() == '':
            error_msg.append('Hour')
        if self.running_time_text.get() == '':
            error_msg.append('Running time')

        if len(self.members_tree.get_checked()) == 0:
            error_msg.append('Members (at least one)')
        if len(self.cats_tree.get_checked()) == 0:
            error_msg.append('Categories (at least one)')

        if self.debate.get() == 1:
            if self.speaker.get() == '':
                error_msg.append('Speaker')
            if self.contact_details.get() == '':
                error_msg.append('Contact details')
        if self.presentation.get() == 1:
            if self.author.get() == '':
                error_msg.append('Author')
            if self.context.get() == '':
                error_msg.append('Context')

        if len(error_msg) == 0:
            return None
        else:
            return ' '.join(['Missing or incorrect fields :', ', '.join(error_msg)])

    def save(self, event=None):
        '''
        Get all the datas from the form to create an
        event. Redirects to the events page
        '''
        error_msg = self.check_missing_or_incorrect_input()

        if error_msg != None:
            print(error_msg)
            self.error_text.set(error_msg)
            return


        new_event = dict()

        log.info("Name " + self.name_entry.get())
        log.info("Day " + self.begin_text.get())
        log.info("Hour " + self.hour_text.get())
        log.info("Running time " + self.running_time_text.get())

        log.info("Projection type " + self.projection_type_choosen.get())
        log.info("Projection room " + self.projection_room_choosen.get())

        new_event['name'] = self.name_entry.get()
        new_event['begin'] = self.begin_text.get() + ' ' + self.hour_text.get() + ':00'
        new_event['running_time'] = self.running_time_text.get()
        new_event['projection_type'] = self.projection_type_choosen.get()
        new_event['projection_room'] = self.projection_room_choosen.get()
        member_names = [self.members_tree.item(member)['text'] for member in self.members_tree.get_checked()]
        cat_titles = [self.cats_tree.item(title)['text'] for title in self.cats_tree.get_checked()]
        event_id = self.controller.create_event(new_event)

        self.controller.create_team(member_names, event_id)
        self.controller.create_events_categories(cat_titles, event_id)
        self.controller.update_events_page()
        self.controller.show_frame("EventsPage")

        # ^(2[0-4]|1[0-9]|[1-9])$

class Spinbox(ttk.Entry):

    def __init__(self, master=None, **kw):

        ttk.Entry.__init__(self, master, 'ttk::spinbox', **kw)

