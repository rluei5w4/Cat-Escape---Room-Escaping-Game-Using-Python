"""
COMP.CS.100 week 13 Python program.
Project: Graphical User Interface
Student id number: 151792018
Email: yifan.zhou@tuni.fi
"""

"""
This project is a room-escaping role-playing game.
The player needs to help the cat to sneak out of the house.
This game is implemented through an advanced GUI since a
radiobutton-type component is included, as well as all kinds
of data structures: list, set and dictionary.
"""

from tkinter import *

class RoomEscapeGame:
    def __init__(self):
        self.__main_window = Tk()
        self.__main_window.title('Cat Escape')

        # The cat will collect items in the house.
        # Some of the furnitures can only be accessed when certain items.
        # Sometimes the cat needs a certain number of items to access some places.
        # So a dictionary is needed to store the names of the items and their numbers.
        self.__cat_items = {}

        # There are four rooms in the game. Each of them has an image,
        # clearly informing the player of the current location.
        self.__rooms_file = {'Living Room':'living room.png',
                             'Kitchen':'kitchen.png',
                             'Bedroom':'bedroom.png',
                             'Bathroom':'bathroom.png'}

        # The items can only be collected once from the same furniture.
        # Since set only contains unique data, it is used here to store the furnitures.
        # If a furniture is already in the set, then the furniture is deemed as empty
        # and nothing can be collected from it.
        self.__empty_places = set()

        # In the bedroom there will be an event requiring password.
        # After the laptop is unlocked, False will turn into True.
        # This is to make sure that when clicking the laptop after it is unlocked,
        # no password is required again.
        self.__bedroom_events = {'Laptop': False}

        # The title of the game
        self.__title_label = Label(self.__main_window,text='Cat Escape')
        self.__title_label.grid(row=0,column=0,columnspan=4)

        # Set the default landing room when the game starts.
        # The default can be changed to other options,
        # so it would be suitable to make it as a variable and change it later.
        self.__current_room = StringVar(value='Living Room')
        self.display_room()

        # Below the game title, there are four radiobuttons.
        # The value of the variable 'self.__current_room' is changed
        # when every radiobutton is clicked.
        self.__radiobutton1 = Radiobutton(self.__main_window, text='Living Room',
                                          variable=self.__current_room,
                                          value='Living Room',
                                          command=self.display_room)
        self.__radiobutton1.grid(row=1, column=0)
        self.__radiobutton2 = Radiobutton(self.__main_window, text='Kitchen',
                                          variable=self.__current_room,
                                          value='Kitchen',
                                          command=self.display_room)
        self.__radiobutton2.grid(row=1, column=1)
        self.__radiobutton3 = Radiobutton(self.__main_window, text='Bedroom',
                                          variable=self.__current_room,
                                          value='Bedroom',
                                          command=self.display_room)
        self.__radiobutton3.grid(row=1, column=2)
        self.__radiobutton4 = Radiobutton(self.__main_window, text='Bathroom',
                                          variable=self.__current_room,
                                          value='Bathroom',
                                          command=self.display_room)
        self.__radiobutton4.grid(row=1, column=3)

        # Below the room images there is the dialogue field of the cat.
        # The cat has a profile photo in front of her dialogue, just like in most RPGs.
        # I made the dialogue field into a text widget instead of a label one,
        # so that it looks good.
        self.__cat = PhotoImage(file='cat.png')
        self.__cat_image = Label(self.__main_window, image=self.__cat)
        self.__cat_image.grid(row=8,column=0,sticky=E)

        self.__cat_text = Text(self.__main_window,height=8,width=50,wrap=WORD)
        self.__cat_text.grid(row=8,column=1,columnspan=4,sticky=W)
        self.__cat_text.insert(END, 'My name is Snowball. I live with a human.\n'
                                    '\nIt\'s a wonderful night. '
                                    'I feel so bored inside the house.\n'
                                    '\nI\'ll find a way out now that nobody else is at home.')
        self.__cat_text.config(state=DISABLED)
        # I do not want the player to input texts and mess up the cat's words,
        # so the widget is usually set as disabled.

        # Below the cat's dialogue, there are some buttons that are interactive throughout the game.
        # When 'Check items' is clicked, the cat will count all her items in an alphabetical order.
        # When 'Restart' is clicked, the game is aborted and the player is brought back
        # to the starting point of a new game.
        # 'Quit' button is used to quit the game.
        self.__check = Button(self.__main_window,text='Check Items',
                                    command=self.check_items)
        self.__check.grid(row=9,column=2)
        self.__restart = Button(self.__main_window,text='Restart',command=self.reset)
        self.__restart.grid(row=9,column=3)
        self.__quit = Button(self.__main_window,text='Quit',command=self.quit)
        self.__quit.grid(row=9,column=4)

    def start(self):
        self.__main_window.mainloop()

    def display_room(self):
        """When each radiobutton is clicked, a function self.display_room() is called.
        This function will show the corresponding image and buttons of each room.
        Before each room is displayed, the buttons from the previous room is deleted
        to avoid possible clashes and overlapping."""

        room = self.__current_room.get()
        self.__room_photoimage = PhotoImage(file=self.__rooms_file[room])
        self.__room_image = Label(self.__main_window, image=self.__room_photoimage)
        self.__room_image.grid(row=2, column=1, columnspan=2,rowspan=2)
        self.delete_buttons(2, 0)
        self.delete_buttons(3, 0)
        self.delete_buttons(2, 3)
        self.delete_buttons(3, 3)
        self.delete_buttons(6, 0)
        self.delete_buttons(6, 1)
        self.delete_buttons(6, 2)
        self.delete_buttons(7, 0)
        self.delete_buttons(7, 1)
        self.delete_buttons(7, 2)

        # Different rooms have different buttons and events.
        # It is not that easy for the buttons and events to be called directly like images.
        # So I store them into different functions.
        if room == "Living Room":
            self.display_living_room()
        elif room == "Kitchen":
            self.display_kitchen()
        elif room == "Bedroom":
            self.display_bedroom()
        elif room == "Bathroom":
            self.display_bathroom()

    def display_living_room(self):
        """This function creates four buttons inside the living room."""

        self.__door = Button(self.__main_window,text='Door',command=self.check_door)
        self.__door.grid(row=2,column=0)
        self.__coffee_table = Button(self.__main_window,text='Coffee Table',command=self.check_coffee_table)
        self.__coffee_table.grid(row=3,column=0)
        self.__sofa = Button(self.__main_window,text='Sofa',
                             command=lambda:self.collect_item(['Sock','Carton Box','Toy Ball'],
                                                              'Sofa'))
        self.__sofa.grid(row=2,column=3)
        self.__bookshelf = Button(self.__main_window,text='Bookshelf',
                                  command=self.display_calculator)
        self.__bookshelf.grid(row=3,column=3)


    def display_kitchen(self):
        """This function creates four buttons inside the kitchen."""

        self.__fridge = Button(self.__main_window,text='Fridge',
                               command=lambda:self.collect_item(['Canned Cat Food'],'Fridge'))
        self.__fridge.grid(row=2,column=0)
        self.__cupboard = Button(self.__main_window,text='Cupboard',
                                 command=lambda:self.collect_item(['Carton Box','Spoon'],'Cupboard'))
        self.__cupboard.grid(row=3, column=0)
        self.__upper_cabinet = Button(self.__main_window,text='Upper Cabinet',
                                      command=self.count_carton_box)
        self.__upper_cabinet.grid(row=2,column=3)
        self.__stove = Button(self.__main_window,text='Stove',
                              command=lambda:self.collect_item(['Fried Egg Residue'],'Stove'))
        self.__stove.grid(row=3,column=3)

    def display_bedroom(self):
        """This function creates four buttons inside the bedroom ONLY IF the player has found
        a bedroom key and stored it in the item dictionary. If the player does not have the key,
        then the cat will say that she cannot enter, and no buttons will show in this case."""

        if 'Bedroom Key' not in self.__cat_items:
            self.__cat_text.config(state=NORMAL)
            self.__cat_text.delete('1.0', END)
            self.__cat_text.insert(END, 'Looks like the bedroom door is locked. '
                                        'I need to find a key to open this door.')
            self.__cat_text.config(state=DISABLED)
        else:
            self.__under_the_bed = Button(self.__main_window, text='Under the Bed',
                                      command=lambda: self.collect_item(['Carton Box'], 'Under the Bed'))
            self.__under_the_bed.grid(row=2, column=0)
            self.__laptop = Button(self.__main_window,text='Laptop',
                                   command=self.display_laptop)
            self.__laptop.grid(row=3,column=0)
            self.__desk_drawer=Button(self.__main_window,text='Desk Drawer',
                                      command=self.display_drawer)
            self.__desk_drawer.grid(row=2,column=3)
            self.__wardrobe=Button(self.__main_window,text='Wardrobe',
                                   command=lambda:self.collect_item(['Sock'],'Wardrobe'))
            self.__wardrobe.grid(row=3,column=3)


    def display_bathroom(self):
        """This function creates four buttons inside the bathroom."""

        self.__sink = Button(self.__main_window,text='Sink',
                             command=lambda:self.collect_item(['Cat Fur'],'Sink'))
        self.__sink.grid(row=2,column=0)
        self.__bathtub = Button(self.__main_window,text='Bathtub',
                                command=lambda:self.collect_item(['Cat Fur','Comb','Toy Ball'],'Bathtub'))
        self.__bathtub.grid(row=3,column=0)
        self.__mirror_cabinet = Button(self.__main_window,text='Mirror Cabinet',
                                       command=lambda:self.collect_item(['Bedroom Key'],'Mirror Cabinet'))
        self.__mirror_cabinet.grid(row=2,column=3)
        self.__shower = Button(self.__main_window,text='Shower',
                               command=lambda:self.collect_item(['Dead Mosquito'],'Shower'))
        self.__shower.grid(row=3,column=3)

    def display_password_box(self):
        """This function creates an entry type widget for the player to input password,
        as well as a button to submit the password and check if the password is correct.
        The entry is constantly showing until a correct password is given.
        This is because the password box is an item carried by the player,
        so it would make sense to carry it around the house."""

        if 'Password Box' in self.__cat_items:
            self.__password_label = Label(self.__main_window,text='Password (8 digits)')
            self.__password_label.grid(row=4,column=0,sticky=E)
            self.__password_entry = Entry(self.__main_window)
            self.__password_entry.grid(row=4,column=1)
            self.__password_submit = Button(self.__main_window,text='Open the box',
                                            command=self.check_password)
            self.__password_submit.grid(row=4,column=2,sticky=W)

    def display_calculator(self):
        """This function creates a calculator using an entry type widget
        and a text type widget.
        Similar to the password box, the calculator is an item collected,
        so the widgets created will constantly appear as long as the calculator
        is in the item dictionary.
        The calculator can convert the cat age to human age. A 1-year-old
        cat would be a 15-year-old teenager if it were a human. A 2-year
        -old cat would be 24 years old in human years. After 2 years old,
        every cat year equals to 4 human years."""


        self.collect_item(['Calculator'], 'Bookshelf')
        if 'Calculator' in self.__cat_items:
            self.__cat_age_label = Label(self.__main_window,
                                         text='Cat age (integer from 1 to 25):')
            self.__cat_age_label.grid(row=5,column=0)
            self.__cat_age=Entry(self.__main_window)
            self.__cat_age.grid(row=5,column=1)
            self.__human_age_label = Label(self.__main_window,
                                           text='equals to human age:')
            self.__human_age_label.grid(row=5,column=2)
            self.__human_age=Text(self.__main_window,wrap=WORD,height=1,width=10,state=DISABLED)
            self.__human_age.grid(row=5,column=3)
            self.__calculate_button=Button(self.__main_window,text='Calculate',
                                           command=self.calculate_age)
            self.__calculate_button.grid(row=5,column=4)

    def calculate_age(self):
        """This function converts cat age to human age.
        If nothing is input, then the human age field would be empty.
        If the text input is not a integer between 1 to 25, the human
        age field would show 'NaN'."""

        if self.__cat_age.get():
            try:
                cat_age = int(self.__cat_age.get())
                if cat_age == 1:
                    self.__human_age.config(state=NORMAL)
                    self.__human_age.delete('1.0', END)
                    self.__human_age.insert(END, '15')
                    self.__human_age.config(state=DISABLED)
                elif cat_age > 1 and cat_age <= 25:
                    self.__human_age.config(state=NORMAL)
                    self.__human_age.delete('1.0', END)
                    self.__human_age.insert(END, f'{(cat_age - 2) * 4 + 24}')
                    self.__human_age.config(state=DISABLED)
                else:
                    self.__human_age.config(state=NORMAL)
                    self.__human_age.delete('1.0', END)
                    self.__human_age.insert(END, 'NaN')
                    self.__human_age.config(state=DISABLED)
            except ValueError:
                self.__human_age.config(state=NORMAL)
                self.__human_age.delete('1.0', END)
                self.__human_age.insert(END, 'NaN')
                self.__human_age.config(state=DISABLED)
        else:
            self.__human_age.config(state=NORMAL)
            self.__human_age.delete('1.0', END)
            self.__human_age.insert(END, '')
            self.__human_age.config(state=DISABLED)


    def display_laptop(self):
        """This function creates an entry for the laptop password
        ONLY IF the laptop has never been unlocked. Also a button
        is created to check whether the password is right. If the
        laptop is unlocked, then this funtion will only show the
        content on the laptop screen without creating an entry.

        If the player leaves the bedroom when the laptop password
        is showing, the password entry will disappear. This is
        because the laptop is not an item of the player, and thus
        can only be accessed in the bedroom."""

        if self.__bedroom_events['Laptop']==False:
            self.__laptop_password_label=Label(self.__main_window,
                                               text='Password: What is the name of my cat?\n'
                                                    '(All lowercase)')
            self.__laptop_password_label.grid(row=6,column=0)
            self.__laptop_password=Entry(self.__main_window)
            self.__laptop_password.grid(row=6,column=1)
            self.__laptop_password_submit=Button(self.__main_window,text='Unlock the laptop',
                                                 command=self.check_password_laptop)
            self.__laptop_password_submit.grid(row=6,column=2)
        else:
            self.__cat_text.config(state=NORMAL)
            self.__cat_text.delete('1.0', END)
            self.__cat_text.insert(END, 'The laptop is unlocked!\n'
                                        '\nThe webpage shows a programming course. '
                                        'The course code is CS100.')
            self.__cat_text.config(state=DISABLED)

    def display_drawer(self):
        """This function creates an entry for the drawer password
        ONLY IF the drawer has not been opened. Also a button
        is created to check whether the password is right. If the
        drawer is unlocked, a key will be collected, and additional
        clicks on the drawer button will only lead to a message saying
        the drawer is empty.
        The drawer has three questions. If the player leaves the bedroom
        when the drawer password is showing, the password entry will disappear.
        This is because the drawer is not an item of the player, and thus
        can only be accessed in the bedroom. The player needs to re-enter
        passwords from Question 1 if they leave the bedroom and return."""

        if 'Key' not in self.__cat_items:
            self.delete_buttons(7, 0)
            self.delete_buttons(7, 1)
            self.delete_buttons(7, 2)
            self.__drawer_password1_label=Label(self.__main_window,
                                               text='Drawer Question 1:\nWhat is my name?\n(All lowercase)')
            self.__drawer_password1_label.grid(row=7, column=0)
            self.__drawer_password1 = Entry(self.__main_window)
            self.__drawer_password1.grid(row=7, column=1)
            self.__drawer_password1_submit = Button(self.__main_window, text='Continue',
                                                   command=self.check_password1_drawer)
            self.__drawer_password1_submit.grid(row=7, column=2)
        else:
            self.collect_item(['Key'],'Desk Drawer')


    def collect_item(self,items,place):
        """
        This funtion collects items and stores them into the item dictionary.
        Also it stores the places where the items are found into the furniture set.
        If the player has searched a certain place, the place would be empty, and
        nothing will be added to the dictionary.
        :param items: the items found all oround the house. It is a list, because more than
        one item can be found in a place.
        :param place: the places where items are found. It is a string.
        :return: None
        """
        for item in items:
            item_id = f'{item} {place}'
            if item_id in self.__empty_places:
                self.__cat_text.config(state=NORMAL)
                self.__cat_text.delete('1.0', END)
                self.__cat_text.insert(END, f'{place} is empty. I need to look elsewhere.\n')
                self.__cat_text.config(state=DISABLED)

            else:
                self.__empty_places.add(item_id)
                self.__cat_text.config(state=NORMAL)
                self.__cat_text.delete('1.0', END)
                items_str = ', '.join(items)
                self.__cat_text.insert(END, f'{items_str} collected.\n')
                self.__cat_text.config(state=DISABLED)
                if item in self.__cat_items:
                    self.__cat_items[item] += 1
                else:
                    self.__cat_items[item] = 1


    def check_door(self):
        """This funtion checks whether the house key is in the item dictionary. If
        it is, then the door opens and the game ends. In order to give the player a
        feeling of the game being ended, some of the buttons are deleted from this
        point.
        If the player does not have the key, the game prints out a message and continues."""

        if "Key" in self.__cat_items:
            self.__cat_text.config(state=NORMAL)
            self.__cat_text.delete('1.0',END)
            self.__cat_text.insert(END, 'Cool! Now the door is open.\n'
                                        '\nTime to hang out in the city!\n'
                                        '\nBy the way thank you for helping. '
                                        'You can quit the game now.')
            self.__cat_text.config(state=DISABLED)
            self.delete_buttons(1, 0)
            self.delete_buttons(1, 1)
            self.delete_buttons(1, 2)
            self.delete_buttons(1, 3)
            self.delete_buttons(2, 0)
            self.delete_buttons(3, 0)
            self.delete_buttons(2, 3)
            self.delete_buttons(3, 3)
            self.delete_buttons(4, 0)
            self.delete_buttons(4, 1)
            self.delete_buttons(4, 2)
            self.delete_buttons(5, 0)
            self.delete_buttons(5, 1)
            self.delete_buttons(5, 2)
            self.delete_buttons(5, 3)
            self.delete_buttons(5, 4)
            self.delete_buttons(6, 0)
            self.delete_buttons(6, 1)
            self.delete_buttons(6, 2)
            self.delete_buttons(7, 0)
            self.delete_buttons(7, 1)
            self.delete_buttons(7, 2)

        else:
            self.__cat_text.config(state=NORMAL)
            self.__cat_text.delete('1.0', END)
            self.__cat_text.insert(END, 'The door is locked. '
                                        'I need a key to open this door.')
            self.__cat_text.config(state=DISABLED)

    def check_coffee_table(self):
        """This function collects a pet id if the coffee table is searched for the
        first time. Also it creates a button used to check the content on the pet id.
        The content will be useful when some password is needed to be input, so always
        having a chance to check the content is convenient for the player."""

        if 'Pet Identity Card Coffee Table' not in self.__empty_places:
            self.collect_item(['Pet Identity Card'], 'Coffee Table')
            self.__cat_text.config(state=NORMAL)
            self.__cat_text.insert(END, '\nSeems like this is my ID.\n'
                                        '\nMy birthday is 18-08-2020.\n'
                                        'Maybe I can try to input my birthday '
                                        'when some password is needed somewhere.')
            self.__cat_text.config(state=DISABLED)
            self.check_id()
        else:
            self.collect_item(['Pet Identity Card'], 'Coffee Table')

    def count_carton_box(self):
        """This function counts the number of the carton box in the item dictionary
        and gives different messages based on different numbers.
        Also this function collects the password box if the value of carton boxe is
         3. When the password box is collected, the password entry appears, and the
          cabinet becomes empty."""

        if 'Carton Box' not in self.__cat_items:
            self.__cat_text.config(state=NORMAL)
            self.__cat_text.delete('1.0', END)
            self.__cat_text.insert(END, 'The cabinet is too high for me to jump up on it.\n'
                                        '\nMaybe I can collect the carton boxes in this house'
                                        ' and pile them up, so that I can jump up from the boxes.\n'
                                        f'\nI think I need to find 3 boxes.')
            self.__cat_text.config(state=DISABLED)
        elif self.__cat_items['Carton Box'] < 3:
            self.__cat_text.config(state=NORMAL)
            self.__cat_text.delete('1.0', END)
            self.__cat_text.insert(END, 'The cabinet is too high for me to jump up on it.\n'
                                        '\nMaybe I can collect the carton boxes in this house'
                                        ' and pile them up, so that I can jump up from the boxes. '
                                        f'Now I need {3-self.__cat_items["Carton Box"]} more.')
            self.__cat_text.config(state=DISABLED)
        elif 'Password Box' not in self.__cat_items:
            self.collect_item(['Password Box'],'Upper Cabinet')
            self.display_password_box()
        else:
            self.collect_item(['Password Box'], 'Upper Cabinet')


    def check_password(self):
        """This function checks whether the password for the box is correct.
        If nothing is input in the entry, nothing will happen."""

        if self.__password_entry.get():
            if self.__password_entry.get() == '18082020':
                self.delete_buttons(4, 0)
                self.delete_buttons(4, 1)
                self.delete_buttons(4, 2)
                self.__cat_text.config(state=NORMAL)
                self.__cat_text.delete('1.0', END)
                self.__cat_text.insert(END, 'The box is opened!\n'
                                            '\nSomething is inside. '
                                            'Seems like this is a photo album of me and the human. '
                                            'The cover says \'Mia and Snowball\'.')
                self.__cat_text.config(state=DISABLED)
                self.add_album()
            else:
                self.__cat_text.config(state=NORMAL)
                self.__cat_text.delete('1.0', END)
                self.__cat_text.insert(END, 'The box cannot be opened. '
                                            'I think the password is incorrect.')
                self.__cat_text.config(state=DISABLED)


    def check_password_laptop(self):
        """This function checks whether the password of the laptop is correct.
        If it is, then the laptop is unlocked from then on until the game ends."""

        if self.__laptop_password.get():
            if self.__laptop_password.get() == 'snowball':
                self.delete_buttons(6, 0)
                self.delete_buttons(6, 1)
                self.delete_buttons(6, 2)
                self.__cat_text.config(state=NORMAL)
                self.__cat_text.delete('1.0', END)
                self.__cat_text.insert(END, 'The laptop is unlocked!\n'
                                            '\nThe webpage shows a programming course. '
                                            'The course code is CS100.')
                self.__cat_text.config(state=DISABLED)
                self.__bedroom_events['Laptop'] = True
            else:
                self.__cat_text.config(state=NORMAL)
                self.__cat_text.delete('1.0', END)
                self.__cat_text.insert(END, 'The laptop cannot be unlocked.\n'
                                            '\nI guess the password is wrong.')
                self.__cat_text.config(state=DISABLED)

    def check_password1_drawer(self):
        """This function checks the password for the Question 1 of the drawer.
        If it is correct, then the widgets for Question 1 will be replaced by
        Question 2."""

        if self.__drawer_password1.get():
            if self.__drawer_password1.get()=='mia':
                self.delete_buttons(7, 0)
                self.delete_buttons(7, 1)
                self.delete_buttons(7, 2)
                self.__cat_text.config(state=NORMAL)
                self.__cat_text.delete('1.0', END)
                self.__cat_text.insert(END, 'Yes this is correct. Now there\'s a second question.')
                self.__cat_text.config(state=DISABLED)
                self.__drawer_password2_label = Label(self.__main_window,
                                                      text='Drawer Question 2:\nWhat is my programming course code?\n'
                                                           '(2 uppercase letters and 3 digits)')
                self.__drawer_password2_label.grid(row=7, column=0)
                self.__drawer_password2 = Entry(self.__main_window)
                self.__drawer_password2.grid(row=7, column=1)
                self.__drawer_password2_submit = Button(self.__main_window, text='Continue',
                                                        command=self.check_password2_drawer)
                self.__drawer_password2_submit.grid(row=7, column=2)

            else:
                self.__cat_text.config(state=NORMAL)
                self.__cat_text.delete('1.0', END)
                self.__cat_text.insert(END, 'I cannot continue. I guess the password is wrong.\n'
                                            '\nI think I need to put the human\'s name here.')
                self.__cat_text.config(state=DISABLED)

    def check_password2_drawer(self):
        """This function checks the password for the Question 2 of the drawer.
        If it is correct, then the widgets for Question 2 will be replaced by
        Question 3."""

        if self.__drawer_password2.get():
            if self.__drawer_password2.get()=='CS100':
                self.delete_buttons(7, 0)
                self.delete_buttons(7, 1)
                self.delete_buttons(7, 2)
                self.__cat_text.config(state=NORMAL)
                self.__cat_text.delete('1.0', END)
                self.__cat_text.insert(END, 'Yes this is correct. Now there\'s the third question.')
                self.__cat_text.config(state=DISABLED)
                self.__drawer_password3_label = Label(self.__main_window,
                                                      text='Drawer Question 3:\n'
                                                           'What would be the age of my cat in Year 2023\n'
                                                           'if she were a human?')
                self.__drawer_password3_label.grid(row=7, column=0)
                self.__drawer_password3 = Entry(self.__main_window)
                self.__drawer_password3.grid(row=7, column=1)
                self.__drawer_password3_submit = Button(self.__main_window,
                                                        text='Unlock the Drawer',
                                                        command=self.check_password3_drawer)
                self.__drawer_password3_submit.grid(row=7, column=2)

            else:
                self.__cat_text.config(state=NORMAL)
                self.__cat_text.delete('1.0', END)
                self.__cat_text.insert(END, 'I cannot continue. I guess the code is wrong.\n'
                                            '\nMaybe I can find the course code somewhere.')
                self.__cat_text.config(state=DISABLED)

    def check_password3_drawer(self):
        """This function checks the password for the Question 3 of the drawer.
        If it is correct, then the drawer is unlocked and becomes empty, while at
        the same time a key is collected. No more passwords are required after the
        drawer is emptied."""

        if self.__drawer_password3.get():
            if self.__drawer_password3.get()=='28':
                self.delete_buttons(7, 0)
                self.delete_buttons(7, 1)
                self.delete_buttons(7, 2)
                self.collect_item(['Key'],'Desk Drawer')

            else:
                self.__cat_text.config(state=NORMAL)
                self.__cat_text.delete('1.0', END)
                self.__cat_text.insert(END, 'I cannot unlock the drawer. I guess the password is wrong.\n'
                                            '\nI think I can try to calculate the answer using something '
                                            'in the house.')
                self.__cat_text.config(state=DISABLED)


    def reset(self):
        """This function aborts the current game and starts a new game."""

        self.__cat_items.clear()
        self.__empty_places.clear()
        self.__bedroom_events['Laptop']=False
        self.__radiobutton1 = Radiobutton(self.__main_window, text='Living Room',
                                          variable=self.__current_room,
                                          value='Living Room',
                                          command=self.display_room)
        self.__radiobutton1.grid(row=1, column=0)
        self.__radiobutton2 = Radiobutton(self.__main_window, text='Kitchen',
                                          variable=self.__current_room,
                                          value='Kitchen',
                                          command=self.display_room)
        self.__radiobutton2.grid(row=1, column=1)
        self.__radiobutton3 = Radiobutton(self.__main_window, text='Bedroom',
                                          variable=self.__current_room,
                                          value='Bedroom',
                                          command=self.display_room)
        self.__radiobutton3.grid(row=1, column=2)
        self.__radiobutton4 = Radiobutton(self.__main_window, text='Bathroom',
                                          variable=self.__current_room,
                                          value='Bathroom',
                                          command=self.display_room)
        self.__radiobutton4.grid(row=1, column=3)
        self.delete_buttons(4, 0)
        self.delete_buttons(4, 1)
        self.delete_buttons(4, 2)
        self.delete_buttons(5, 0)
        self.delete_buttons(5, 1)
        self.delete_buttons(5, 2)
        self.delete_buttons(5, 3)
        self.delete_buttons(5, 4)
        self.delete_buttons(6, 0)
        self.delete_buttons(6, 1)
        self.delete_buttons(6, 2)
        self.delete_buttons(7, 0)
        self.delete_buttons(7, 1)
        self.delete_buttons(7, 2)
        self.delete_buttons(9, 0)
        self.delete_buttons(9, 1)
        self.__cat_text.config(state=NORMAL)
        self.__cat_text.delete('1.0', END)
        self.__cat_text.insert(END, 'My name is Snowball. I live with a human.\n'
                                    '\nIt\'s a wonderful night. '
                                    'I feel so bored inside the house.\n'
                                    '\nI\'ll find a way out now that nobody else is at home.')
        self.__cat_text.config(state=DISABLED)
        self.__current_room.set('Living Room')
        self.display_room()

    def delete_buttons(self,row,column):
        """
        This function delete the certain widget.
        :param row: the row of the widget
        :param column: the column of the widget
        :return: None
        """

        for button in self.__main_window.grid_slaves():
            if int(button.grid_info()['row'])==row and\
                int(button.grid_info()['column']==column):
                button.destroy()

    def check_items(self):
        """This function prints the items in an alphabetical order and prints their number.
        If the player has no item, then a unique message appears."""

        if self.__cat_items == {}:
            self.__cat_text.config(state=NORMAL)
            self.__cat_text.delete('1.0', END)
            self.__cat_text.insert(END, 'I have no items currently.')
            self.__cat_text.config(state=DISABLED)
        else:
            self.__cat_text.config(state=NORMAL)
            self.__cat_text.delete('1.0', END)
            for key,value in sorted(self.__cat_items.items()):
                self.__cat_text.insert(END, f'{key}: {value}\n')
            self.__cat_text.config(state=DISABLED)

    def check_id(self):
        """This function creates a 'check id' button after the id is collected."""

        if 'Pet Identity Card' in self.__cat_items:
            self.__check_id_card = Button(self.__main_window, text='Check ID Card',
                                          command=self.show_id)
            self.__check_id_card.grid(row=9, column=0)

    def show_id(self):
        """This function shows the content of the id when the 'check id' button is clicked."""

        self.__cat_text.config(state=NORMAL)
        self.__cat_text.delete('1.0', END)
        self.__cat_text.insert(END, 'Seems like this is my ID.\n'
                                    '\nMy birthday is 18-08-2020.\n'
                                    'Maybe I can try to input my birthday '
                                    'when some password is needed somewhere.')
        self.__cat_text.config(state=DISABLED)

    def add_album(self):
        """This function creates a 'check album' button after the password box is opened."""

        self.__check_album = Button(self.__main_window, text='Check Album',
                                      command=self.show_album)
        self.__check_album.grid(row=9, column=1)

    def show_album(self):
        """This function shows the information of the album after clicking the 'check album' button."""

        self.__cat_text.config(state=NORMAL)
        self.__cat_text.delete('1.0', END)
        self.__cat_text.insert(END, 'Seems like this is a photo album of me and the human. '
                                    'The cover says \'Mia and Snowball\'.')
        self.__cat_text.config(state=DISABLED)

    def quit(self):
        self.__main_window.destroy()


def main():
    game = RoomEscapeGame()
    game.start()

if __name__=='__main__':
    main()

