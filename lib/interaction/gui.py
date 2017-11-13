from tkinter import *

from lib.booking.destination import Destination
from lib.booking.schedule import Schedule
from lib.occupant import Person
from lib.train.seat import Walkway, SeatBookedError
from lib.train.train import Train
from lib.train.wagon import Wagon


class TrainWindow(object):
    def on_close(self):
        try:
            self.__root.destroy()
        except:
            pass
        self.__master.unhide_window()

    def __init__(self, master, train, user, schedule_index=None):

        self.__master = master
        self.__train = train
        self.__root = Tk()

        self.__root.geometry("1000x250")

        if schedule_index is not None:
            self.schedule_index = schedule_index
        else:
            self.schedule_index = self.__train.get_max_length_travel()

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
        train_frame = Frame(self.__root, pady=10, padx=10)

        for tindex in range(self.__train.get_wagons().__len__()):
            wagon = self.__train[tindex]

            wagon_frame = Frame(train_frame, pady=10, padx=10)
            a = Label(train_frame, text="Wagon: {}".format(wagon.get_wagon_number()))

            for index in range(wagon.__len__()):
                row = wagon[index]
                for jndex in range(row.__len__()):
                    seat_i = row[jndex]
                    temp_btn = None
                    if isinstance(seat_i, Walkway):
                        temp_btn = Label(wagon_frame,  # text=seat_i.seat_is_booked([0]),
                                         height=self.btn_book_height, width=self.btn_book_width)

                    else:
                        temp_btn = Button(wagon_frame, text=seat_i.get_seat_number(),
                                          command="", height=self.btn_book_height, width=self.btn_book_width)
                    temp_btn.grid(column=index, row=jndex)
                    temp_btn["state"] = "disable"
                    seat_i.set_button(temp_btn)

            wagon_frame.grid(column=tindex, row=1)
            a.grid(column=tindex, row=0)
        train_frame.pack(side=LEFT)

    def create_main_buttons(self):
        main_frame = Frame(self.__root, height=1, width=1, pady=10, padx=10)

        self.btn_book = Button(main_frame, text="Book",
                               command=lambda: self.book_fixed(), height=self.btn_height,
                               width=self.btn_width)

        self.input_number = Entry(main_frame)

        self.btn_exit = Button(main_frame, text="Exit booking",
                               command=lambda: self.exit_window(), height=self.btn_height, width=self.btn_width)

        Label(main_frame,text="Tap seats to book or\nenter the number of\nseats to book").pack()
        self.input_number.pack(pady=5, padx=10)
        self.btn_book.pack(pady=5)
        self.btn_exit.pack(pady=5)

        main_frame.pack(side=LEFT)

    def exit_window(self):
        self.__root.destroy()
        self.__master.unhide_window()

    def exit_booking(self):
        # self.btn_book["text"] = "Book Trip"
        self.__train.change_button_states("disable")
        # self.btn_book["command"] = lambda: self.init_booking()

    def init_booking(self):
        # self.btn_book["text"] = "Exit Booking"
        # self.btn_book["command"] = lambda: self.exit_booking()
        self.__train.change_button_states("normal")
        self.__train.set_button_command(
            lambda x: self.update_seat_button_booking_color(x, self.schedule_index, self.current_user))

    def update_seat_button_booking_color(self, seat, stops, occupant):
        if not isinstance(stops, list):
            stops = [stops]
        try:
            seat.book(self.schedule_index, occupant)
        except SeatBookedError:
            import tkinter.messagebox
            tkinter.messagebox.showinfo("Seat is aldready booked", "The seat you are trying to book is"
                                                                   "\nalready booked by someone else")
            print("Seat is already booked")
        # seat.set_button_text(lambda x:x.is_booked(stops))
        self.__train.update_buttons(stops, occupant)

    def display(self):
        self.__root.title(self.__train.window_header_display())
        self.__root.mainloop()

    def book_fixed(self):
        number_to_book = self.get_number_of_seat_to_book_input()
        if number_to_book is None:
            return
        if self.__train.get_number_of_free_seats(self.schedule_index) >= number_to_book:
            booked_seats = self.__train.book_number(self.schedule_index, number_to_book, self.current_user)
            if number_to_book - booked_seats > 0:
                import tkinter.messagebox
                answer = tkinter.messagebox.askyesno("Allow split", "No seat found in a single row\n"
                                                                    "Do you want seats on different rows?")
                if answer:
                    print("SPLITING SEATS")
                    self.__train.book_number(self.schedule_index, number_to_book, self.current_user, True)
            return True
        else:
            print("not enough seats")
            return False

    def get_number_of_seat_to_book_input(self):
        try:
            number_of_seats = int(self.input_number.get())
            if not number_of_seats > 0:
                raise ValueError()
        except ValueError:
            import tkinter.messagebox
            tkinter.messagebox.showinfo("Plizz", "Non integer given")
            return None

        return number_of_seats


if __name__ == '__main__':
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
