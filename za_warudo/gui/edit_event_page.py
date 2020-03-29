from functools import partial
from datetime import datetime
from tkinter import *
from tkinter import ttk
import logging as log
import re

import ttkwidgets as tkw

from gui.widgets import EntryDate
from gui.widgets import Spinbox

class EditEventPage(ttk.Frame):
    '''
    Frame to create a new event
    Upon creation the user is redirected to the events page
    TODO frame to create AND edit an event
    '''

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        self.edit_mode = False
        self.event_id = None

        self.error_text = StringVar()
        title = ttk.Label(self, text="Create event", font=("TkDefaultFont", "15"))
        error_label = ttk.Label(self, textvariable=self.error_text, font=("TkDefaultFont", "7"))
        error_label.configure(style="Red.TLabel")
        buttons_frame = ttk.Frame(self)
        back_button = ttk.Button(buttons_frame, text='Back', command=partial(self.controller.show_frame, "EventsPage"))

        # And of course, the button to save it all
        save_button = ttk.Button(buttons_frame, text="Save", command=self.save)

        # Event form
        self.name = StringVar()
        name_label = ttk.Label(self, text="Name")
        self.name_entry = ttk.Entry(self, textvariable=self.name)

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
        # TODO actually we can type anything in this widget
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
        self.room_reserved = IntVar()
        self.management = IntVar()
        self.equipment_reserved = IntVar()
        self.guest_attendance = IntVar()

        check_frame = ttk.Frame(self)
        room_chbutton = ttk.Checkbutton(check_frame, text="Room reserved", variable=self.room_reserved)
        equipment_chbutton = ttk.Checkbutton(check_frame, text="Equipment reserved", variable=self.equipment_reserved)
        management_chbutton = ttk.Checkbutton(check_frame, text="Management reserved", variable=self.management)
        guest_attendance_chbutton = ttk.Checkbutton(check_frame, text="Guest attendance confirmed", variable=self.guest_attendance)



        members_frame = ttk.Frame(self)
        members_label = ttk.Label(self, text="Add members")
        members_scrollbar = ttk.Scrollbar(members_frame, orient=VERTICAL)
        # List of users; the manager has to choose among them
        # members that'll participate in the event's organisation
        self.members_tree = tkw.CheckboxTreeview(members_frame, columns=('Events'), selectmode='browse', yscrollcommand=members_scrollbar.set)
        members_scrollbar.configure(command=self.members_tree.yview)

        self.members_tree.column("Events", anchor='center')
        self.members_tree.heading("#0", text="Name")
        self.members_tree.heading("Events", text="Events")

        self.members_tree.tag_configure('odd', background="#F0F0F0")
        self.members_tree.tag_configure('even', background="#FAFAFA")
        tkw.frames.Balloon(self.members_tree, text='Double click on users to see their timetable')
        self.members_tree.bind('<Double-1>', self.timetable)
        self.display_members(event_id=None)

        # CATEGORIES
        categories_label = ttk.Label(self, text="Add categories")

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

        self.display_categories(event_id=None)

        # PRESENTATION
        self.presentation = IntVar()
        self.author = StringVar()
        self.context = StringVar()

        presentation_frame = ttk.Frame(self)
        presentation_check = ttk.Checkbutton(presentation_frame,
                                             text="Author presentation",
                                             variable=self.presentation)

        # DEBATE
        self.debate = IntVar()
        self.speaker = StringVar()
        self.contact_details = StringVar()

        debate_frame = ttk.Frame(self)
        debate_check = ttk.Checkbutton(debate_frame,
                                       text="Debate",
                                       variable=self.debate)

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
        pj_label.grid(row=3, column=0, sticky=W, pady=5, padx=5)
        projection_types.grid(row=3, column=1, sticky=E, pady=5, padx=5)
        pr_label.grid(row=3, column=2, pady=5, sticky=W, padx=5)
        projection_rooms.grid(row=3, column=3, sticky=E, pady=5, padx=5)

        # ROW 0 RIGHT SIDE
        presentation_frame.grid(row=1, column=4, sticky=NSEW, columnspan=2, rowspan=2, pady=5, padx=5)
        presentation_check.grid(row=0, column=0, sticky=W)

        # ROW 3 RIGHT SIDE
        debate_frame.grid(row=3, column=4, sticky=NSEW, rowspan=2, columnspan=2, pady=5, padx=5)
        debate_check.grid(row=0, column=0, sticky=W)

        # ROW 5 RIGHT SIDE
        check_frame.grid(row=5, column=4, rowspan=2, columnspan=2, sticky=N+W, pady=5, padx=5)
        room_chbutton.grid(row=4, column=2, sticky=W)
        equipment_chbutton.grid(row=5, column=2, sticky=W)
        management_chbutton.grid(row=6, column=2, sticky=W)
        guest_attendance_chbutton.grid(row=7, column=2, sticky=W)

        # ROW 6
        members_frame.grid(row=5, column=0, columnspan=2, pady=5, padx=5, sticky=NSEW)
        members_label.grid(row=4, column=0, pady=5, padx=5, sticky=W)
        self.members_tree.pack(side=LEFT)
        members_scrollbar.pack()

        categories_label.grid(row=4, column=2, pady=5, padx=5, sticky=W)
        cats_frame.grid(row=5, column=2, columnspan=2, pady=5, padx=5, sticky=NSEW)
        self.cats_tree.pack(side=LEFT, expand=True)
        cats_scrollbar.pack()

    def check_missing_or_incorrect_input(self) -> str:
        '''
        Name, day, hour, running time, must not be empty
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

        if len(error_msg) == 0:
            return None
        else:
            return ' '.join(['Missing or incorrect fields :', ', '.join(error_msg)])

    def is_event_finished(self) -> bool:
        '''
        Check if certain checkboxes are checked
        '''
        return (self.room_reserved.get() == 1 and self.management.get() == 1
                and self.equipment_reserved.get() == 1 and self.guest_attendance.get() == 1)

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

        new_event['room_reserved'] = self.room_reserved.get() == 1
        new_event['management'] = self.management.get() == 1
        new_event['equipment_reserved'] = self.equipment_reserved.get() == 1
        new_event['guest_attendance'] = self.guest_attendance.get() == 1

        member_names = [self.members_tree.item(member)['text'] for member in self.members_tree.get_checked()]
        cat_titles = [self.cats_tree.item(title)['text'] for title in self.cats_tree.get_checked()]

        log.info("Name " + self.name_entry.get())
        log.info("Day " + self.begin_text.get())
        log.info("Hour " + self.hour_text.get())
        log.info("Running time " + self.running_time_text.get())

        log.info("Projection type " + self.projection_type_choosen.get())
        log.info("Projection room " + self.projection_room_choosen.get())

        log.info(member_names)
        log.info(cat_titles)

        new_event['name'] = self.name_entry.get()
        new_event['begin'] = self.begin_text.get() + ' ' + self.hour_text.get() + ':00'
        new_event['running_time'] = self.running_time_text.get()
        new_event['projection_type'] = self.projection_type_choosen.get()
        new_event['projection_room'] = self.projection_room_choosen.get()

        new_event['debate'] = self.debate.get() == 1
        new_event['presentation'] = self.presentation.get() == 1

        if self.edit_mode:
            if self.event.status == 'in progress' and self.is_event_finished():
                new_event['status'] = 'finished'
            self.controller.update_event(new_event, self.event_id)
            self.controller.update_team(member_names, self.event_id)
            self.controller.update_events_categories(cat_titles, self.event_id)
        else:
            event_id = self.controller.create_event(new_event)
            self.controller.create_team(member_names, event_id)
            self.controller.create_events_categories(cat_titles, event_id)
        self.controller.update_events_page()
        self.controller.show_frame("EventsPage")

    def set_event(self, event: Event):
        self.event = event

    def set_projection_room(self, projection_room):
        self.projection_room = projection_room

    def set_inputs(self):
        '''
        Set the inputs of the page for a given event
        '''

        self.name.set(self.event.name)
        day = self.event.begin.strftime('%Y-%m-%d')
        hour = self.event.begin.strftime('%H')
        self.begin_text.set(day)
        self.hour_text.set(hour)
        self.running_time_text.set(self.event.running_time)
        self.projection_type_choosen.set(self.event.projection_type)
        self.projection_room_choosen.set(self.projection_room.location)


        if self.event.room_reserved:
            self.room_reserved.set(1)
        else:
            self.room_reserved.set(0)

        if self.event.management:
            self.management.set(1)
        else:
            self.management.set(0)

        if self.event.equipment_reserved:
            self.equipment_reserved.set(1)
        else:
            self.equipment_reserved.set(0)

        if self.event.guest_attendance:
            self.guest_attendance.set(1)
        else:
            self.guest_attendance.set(0)

        self.display_members(event_id=self.event.id)
        self.display_categories(event_id=self.event.id)
        self.event_id = self.event.id

    def display_members(self, event_id: int=None):
        '''
        Fill the members treeview
        '''

        self.members_tree.delete(*self.members_tree.get_children())
        users = self.controller.get_events_per_user(event_id)

        for i in range(len(users)):
            self.members_tree.insert('', 'end', iid=str(i), text=users[i]['user'], tags=('even' if i % 2 else 'odd',), values=(users[i]['events'],))
            self.members_tree.change_state(str(i), users[i]['checked'])

    def display_categories(self, event_id: int=None):
        '''
        Fill the categories treeview
        '''

        # The tree is cleaned
        self.cats_tree.delete(*self.cats_tree.get_children())
        # We get the categories realted to the event
        categories = self.controller.get_events_categories(event_id)

        for i, category in enumerate(categories):
            s = '%d%s' % (category['price'], ' €')
            self.cats_tree.insert('', 'end', iid=str(i), text=category['title'], tags=('even' if i % 2 else 'odd',), values=(s,))
            self.cats_tree.change_state(str(i), category['checked'])

    def timetable(self, event=None):
        '''
        Pop up a timetable of a user
        Triggered when there's a click on one of the
        treeview's row
        '''
        item = self.members_tree.selection()[0]
        user_name = self.members_tree.item(item, 'text')
        self.controller.pop_timetable(user_name)


    def set_edit_mode(self):
        self.edit_mode = True

    def set_new_mode(self):
        self.edit_mode = False

