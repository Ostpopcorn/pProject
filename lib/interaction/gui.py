from tkinter import *

from lib.booking.destination import Destination
from lib.booking.schedule import Schedule
from lib.occupant import Person
from lib.train.seat import Walkway, SeatBookedError
from lib.train.train import Train
from lib.train.wagon import Wagon

t = Train("X8000")
t.add_wagon(Wagon(1, 6, 4))
t.add_wagon(Wagon(2, 4, 5))
t.add_wagon(Wagon(3, 2, 3))
ob = Schedule() 
ob.add_destination(Destination("Fjollträsk"))
ob.add_destination(Destination("Mesberg"))
ob.add_destination(Destination("Sumptuna"))
t.set_schedule(ob)
#a = Person("Sven")
#b = Person("Sverker")
# t[0][0][0].book([0, 1], a)
# t[0][0][0].book([0], a)
# t[0][0][0].book([1], b)

seat = t[0][0][0]


class TrainWindow(object):
    def __init__(self, train,user,schedule_index):
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
        self.create_main_buttons()
        self.create_train_buttons()
        self.current_user = user
        self.schedule_index = schedule_index
        # self.__train[0][0][1].book([0], a)
        # self.__train[0][0][1].book([1], b)

    def create_train_buttons(self):
        train_frame = Frame(self.__root, pady=10, padx=10)

        for tindex in range(self.__train.wagons.__len__()):
            wagon =self.__train[tindex]

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
        self.btn_cancel = Button(main_frame, text="Cancel trip",
                                 command=lambda: t.set_button_text(lambda x: x.get_seat_number()),
                                 height=self.btn_height,
                                 width=self.btn_width)
        self.btn_get_ticket = Button(main_frame, text="Get yo tickets",
                                     command=lambda: t.change_button_states("normal"), height=self.btn_height,
                                     width=self.btn_width)
        self.btn_exit = Button(main_frame, text="Exit",
                               command=lambda: main_frame.quit(), height=self.btn_height, width=self.btn_width)
        self.btn_book.pack()
        self.btn_cancel.pack()
        self.btn_get_ticket.pack()
        self.btn_exit.pack()

        main_frame.pack(side=LEFT)

    def exit_booking(self):
        self.btn_book["text"] = "Book Trip"
        for i in [self.btn_cancel, self.btn_get_ticket]:
            i["state"] = "normal"
        self.__train.change_button_states("disable")
        self.btn_book["command"] = lambda: self.init_booking()

    def init_booking(self):
        self.btn_book["text"] = "Exit Booking"
        self.btn_book["command"] = lambda: self.exit_booking()
        for i in [self.btn_cancel, self.btn_get_ticket]:
            i["state"] = "disable"
        self.__train.change_button_states("normal")
        self.__train.set_button_command(lambda x: self.update_seat_button_booking_color(x, [0], self.current_user))

    def update_seat_button_booking_color(self, seat, stops, occupant):
        if not isinstance(stops, list):
            stops = [stops]
        try:
            seat.book([0], occupant)
        except SeatBookedError:
            print("Seat is already booked")
        # seat.set_button_text(lambda x:x.is_booked(stops))
        t.update_buttons(stops, occupant)

    def display(self):
        self.__root.mainloop()


def main_menu():
    btn_height = 1
    btn_width = 15

    main_root = Tk()
    main_frame = Frame(main_root, height=1, width=1, pady=10, padx=10)
    main_root.geometry("1000x250")
    btn_book_text = StringVar()
    btn_book_text.set("Book trip")
    btn_cancel_text = StringVar()
    btn_cancel_text.set("Cancel trip")
    btn_get_ticket_text = StringVar()
    btn_get_ticket_text.set("Get yo tickets")
    btn_exit_text = StringVar()
    btn_exit_text.set("Exit")

    btn_book = Button(main_frame, textvariable=btn_book_text,
                      command=lambda: t.set_button_text(lambda x: x.is_booked([0])), height=btn_height, width=btn_width)
    btn_cancel = Button(main_frame, textvariable=btn_cancel_text,
                        command=lambda: t.set_button_text(lambda x: x.get_seat_number()), height=btn_height,
                        width=btn_width)
    btn_get_ticket = Button(main_frame, textvariable=btn_get_ticket_text,
                            command=lambda: t.change_button_states("normal"), height=btn_height, width=btn_width)
    btn_exit = Button(main_frame, textvariable=btn_exit_text,
                      command=lambda: main_frame.quit(), height=btn_height, width=btn_width)

    wagon_frames = []
    train_frame = Frame(main_root, pady=10, padx=10)

    for tindex in range(t.wagons.__len__()):
        wagon = t[tindex]

        wagon_frame = Frame(train_frame, pady=10, padx=10)
        a = Label(train_frame, text=wagon.get_wagon_number(),
                  height=btn_height, width=btn_width)

        for index in range(wagon.__len__()):
            row = wagon[index]
            for jndex in range(row.__len__()):
                seat_i = row[jndex]
                temp_btn = None
                if isinstance(seat_i, Walkway):
                    temp_btn = Label(wagon_frame,  # text=seat_i.seat_is_booked([0]),
                                     height=btn_height // 2, width=btn_width // 4)

                else:
                    temp_btn = Button(wagon_frame, text=seat_i.get_seat_number(),
                                      command="", height=btn_height // 2, width=btn_width // 4)
                temp_btn.grid(column=index, row=jndex)
                seat_i.set_button(temp_btn)

        wagon_frame.grid(column=tindex, row=1)
        a.grid(column=tindex, row=0)
    # t.print_nice_2(lambda x: x.is_booked([0]))
    t.set_button_command(lambda x: x.book([0], a))
    btn_book.grid()
    btn_cancel.grid()
    btn_get_ticket.grid()
    btn_exit.grid()
    main_frame.grid(column=0, row=0)
    train_frame.grid(column=1, row=0)
    t.change_button_states("disabled")
    main_root.mainloop()

if __name__ == '__main__':
    print("HAHAHAHAHA")
    # main_menu()
    ob = TrainWindow(t)
    ob.display()
