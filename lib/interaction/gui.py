from tkinter import *

from lib.booking.destination import Destination
from lib.booking.schedule import Schedule
from lib.occupant import Person
from lib.train.seat import Walkway, SeatBookedError
from lib.train.train import Train
from lib.train.wagon import Wagon


class TrainWindow(object):
    def __init__(self, train, user, schedule_index):
        self.__train = train
        self.__root = Tk()
        self.__root.geometry("1000x250")
        self.btn_book = None
        self.btn_cancel = None
        self.btn_get_ticket = None
        self.btn_exit = None
        self.btn_height = 1
        self.btn_width = 15
        self.btn_book_width = 2
        self.btn_book_height = 1
        self.current_user = user
        self.schedule_index = schedule_index

        self.create_main_buttons()
        self.create_train_buttons()

        self.__train.update_buttons(self.schedule_index,self.current_user)

    def create_train_buttons(self):
        train_frame = Frame(self.__root, pady=10, padx=10)

        for tindex in range(self.__train.wagons.__len__()):
            wagon = self.__train[tindex]

            wagon_frame = Frame(train_frame, pady=10, padx=10)
            a = Label(train_frame, text=wagon.get_wagon_number())

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

        self.btn_book = Button(main_frame, text="Book trip",
                               command=lambda: self.init_booking(), height=self.btn_height,
                               width=self.btn_width)
        # self.btn_cancel = Button(main_frame, text="Cancel trip",
        #                          command=lambda: self.__train.set_button_text(lambda x: x.get_seat_number()),
        #                          height=self.btn_height,
        #                          width=self.btn_width)
        self.btn_get_ticket = Button(main_frame, text="Get yo tickets",
                                     command=lambda: self.__train.change_button_states("normal"),
                                     height=self.btn_height,
                                     width=self.btn_width)
        self.btn_exit = Button(main_frame, text="Exit",
                               command=lambda: self.exit_window(), height=self.btn_height, width=self.btn_width)
        self.btn_book.pack()
        #self.btn_cancel.pack()
        self.btn_get_ticket.pack()
        self.btn_exit.pack()

        main_frame.pack(side=LEFT)

    def exit_window(self):
        self.__root.quit()

    def withdraw_root(self):
        # self.__root.withdraw()
        pass

    def exit_booking(self):
        self.btn_book["text"] = "Book Trip"
        for i in [self.btn_get_ticket]:
            i["state"] = "normal"
        self.__train.change_button_states("disable")
        self.btn_book["command"] = lambda: self.init_booking()

    def init_booking(self):
        self.btn_book["text"] = "Exit Booking"
        self.btn_book["command"] = lambda: self.exit_booking()
        for i in [self.btn_get_ticket]:
            i["state"] = "disable"
        self.__train.change_button_states("normal")
        self.__train.set_button_command(lambda x: self.update_seat_button_booking_color(x, self.schedule_index, self.current_user))

    def update_seat_button_booking_color(self, seat, stops, occupant):
        if not isinstance(stops, list):
            stops = [stops]
        try:
            seat.book(self.schedule_index, occupant)
        except SeatBookedError:
            print("Seat is already booked")
        # seat.set_button_text(lambda x:x.is_booked(stops))
        self.__train.update_buttons(stops, occupant)

    def display(self):
        self.__root.mainloop()


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
