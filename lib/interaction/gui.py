from tkinter import *


class TrainWindow(object):
    """Window for booking on individual train"""

    def __init__(self, master, train, user, schedule_index=None):
        """Initializes variables and creates buttons according to given trains."""
        self.__master = master
        self.__train = train
        self.__root = Tk()

        self.__root.geometry("1000x250")

        if schedule_index is not None:
            self.schedule_index = schedule_index
        else:
            self.schedule_index = self.__train.get_max_length_travel()

        # Triggers when window is closed
        self.__root.protocol("WM_DELETE_WINDOW", lambda: self.on_close())

        self.btn_book = None
        self.input_number = None
        self.btn_exit = None
        self.btn_height = 1
        self.btn_width = 15
        self.btn_book_width = 2
        self.btn_book_height = 1
        self.current_user = user
        self.create_main_buttons()
        self.create_train_buttons()

        self.__train.update_buttons(self.schedule_index, self.current_user)
        self.init_booking()

    def create_train_buttons(self):
        """Creates buttons corresponding to the __train"""
        train_frame = Frame(self.__root, pady=10, padx=10)

        wagon_bg = "silver"

        # Loop for each wagon
        for train_index in range(self.__train.get_wagons().__len__()):
            wagon = self.__train[train_index]

            wagon_frame = Frame(train_frame, pady=10, padx=10, bg=wagon_bg)
            a = Label(train_frame, text="Wagon: {}".format(wagon.get_wagon_number()))

            wagon_frame.grid(column=train_index, row=1, padx=2)
            a.grid(column=train_index, row=0)

            # Loops for creating all seat butotns
            for row_index in range(wagon.__len__()):
                row = wagon[row_index]
                for column_index in range(row.__len__()):
                    current_seat = row[column_index]
                    # Creates a button for all seat
                    # If the seat is of type walkway a blank label i created to fill the space
                    from lib.train.seat import Walkway
                    if isinstance(current_seat, Walkway):
                        temp_btn = Label(wagon_frame, text="", bg=wagon_bg,  # text=current_seat.seat_is_booked([0]),
                                         height=self.btn_book_height, width=self.btn_book_width)

                    else:
                        temp_btn = Button(wagon_frame, text=current_seat.get_seat_number(),
                                          command="", height=self.btn_book_height, width=self.btn_book_width)
                    # Packs on correct place
                    temp_btn.grid(column=row_index, row=column_index)
                    current_seat.set_button(temp_btn)

        train_frame.pack(side=LEFT)

    def create_main_buttons(self):
        """Creates the button on the left."""
        # A frame is used to group
        main_frame = Frame(self.__root, height=1, width=1, pady=10, padx=10)

        self.btn_book = Button(main_frame, text="Book",
                               command=lambda: self.book_fixed(), height=self.btn_height,
                               width=self.btn_width)

        self.input_number = Entry(main_frame)

        self.btn_exit = Button(main_frame, text="Exit booking",
                               command=lambda: self.exit_window(), height=self.btn_height,
                               width=self.btn_width)

        # The text is constant so its not needed for later and is packed immediately
        Label(main_frame, text="Tap seats to book or\nenter the number of\nseats to book").pack()

        self.input_number.pack(pady=5, padx=10)
        self.btn_book.pack(pady=5)
        self.btn_exit.pack(pady=5)

        main_frame.pack(side=LEFT)

    def exit_window(self):
        """Destroys current Tk instace."""
        self.__root.destroy()
        self.on_close()

    def init_booking(self):
        """Operations for enabling booking."""
        self.__train.set_button_command(
            lambda x: self.update_seat_button_booking_color(x, self.schedule_index, self.current_user))

    def update_seat_button_booking_color(self, seat, stops, occupant):
        """OnClick action for all seat_buttons. Books seat and updates color"""
        if not isinstance(stops, list):
            stops = [stops]
        try:
            seat.book(self.schedule_index, occupant)
        except SeatBookedError:
            # Executes when seat is booked by someone else.
            import tkinter.messagebox
            tkinter.messagebox.showinfo("Seat is aldready booked", "The seat you are trying to book is"
                                                                   "\nalready booked by someone else")
            print("Seat is already booked")
        # Train updates all of its seats button
        self.__train.update_buttons(stops, occupant)

    def display(self):
        """Starts mainloop and sets title"""
        self.__root.title(self.__train.window_header_display())
        self.__root.mainloop()

    def book_fixed(self):
        """Books a set number of seats in the train."""
        number_to_book = self.get_number_of_seat_to_book_input()
        if number_to_book is None:
            return
        # Number of seats to book must be fewer then total number of free seats
        if self.__train.get_number_of_free_seats(self.schedule_index) >= number_to_book:
            # function returns number of seats booked
            booked_seats = self.__train.book_number(self.schedule_index, number_to_book, self.current_user)
            if number_to_book - booked_seats > 0:
                # if non are book then all seat worn't found in one row. But enough seats are available
                # so if it's allowed to split it can fit in the train
                import tkinter.messagebox
                answer = tkinter.messagebox.askyesno("Allow split", "No seat found in a single row\n"
                                                                    "Do you want seats on different rows?")
                if answer:
                    print("SPLITING SEATS")
                    self.__train.book_number(self.schedule_index, number_to_book, self.current_user, True)
            return True
        else:
            import tkinter.messagebox
            tkinter.messagebox.showinfo("Error", "Not enough free seats")
            print("not enough seats")
            return False

    def get_number_of_seat_to_book_input(self):
        """Gets the value in book_number InputBox"""
        try:
            number_of_seats = int(self.input_number.get())
            if not number_of_seats > 0:
                raise ValueError()
        except ValueError:
            import tkinter.messagebox
            tkinter.messagebox.showinfo("Plizz", "Non integer given")
            return None

        return number_of_seats

    def on_close(self):
        """Called when the Tk window is closed."""
        self.__master.unhide_window()
        try:
            self.__root.destroy()
        except:
            pass


if __name__ == '__main__':
    from lib.booking.destination import Destination
    from lib.booking.schedule import Schedule
    from lib.occupant import Person
    from lib.train.seat import Walkway, SeatBookedError
    from lib.train.train import Train
    from lib.train.wagon import Wagon

    print("HAHAHAHAHA")
    t = Train("X8000")
    t.add_wagon(Wagon(1, 6, 4))
    t.add_wagon(Wagon(2, 4, 5))
    t.add_wagon(Wagon(3, 2, 3))
    ob = Schedule()
    ob.add_destination(Destination("Fjollträsk"))
    ob.add_destination(Destination("Mesberg"))
    ob.add_destination(Destination("Sumptuna"))
    t.set_schedule(ob)
    a = Person(1234, "Sven")
    b = Person(4321, "Sverker")
    # t[0][0][0].book([0, 1], a)
    # t[0][0][0].book([0], a)
    # t[0][0][0].book([1], b)



    ob = TrainWindow(t, a, [0, 1])
    ob.display()
