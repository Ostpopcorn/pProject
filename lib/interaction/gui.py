from tkinter import *

from lib.booking.destination import Destination
from lib.booking.schedule import Schedule
from lib.occupant import Person
from lib.train.seat import Walkway
from lib.train.train import Train
from lib.train.wagon import Wagon

t = Train("X8000")
t.add_wagon(Wagon(1, 4, 4))
t.add_wagon(Wagon(2, 2, 5))
t.add_wagon(Wagon(3, 6, 3))
ob = Schedule()
ob.add_destination(Destination("Fjollträsk"))
ob.add_destination(Destination("Mesberg"))
ob.add_destination(Destination("Sumptuna"))
t.set_schedule(ob)
a = Person("Sven")
b = Person("Sverker")
# t[0][0][0].book([0, 1], a)
t[0][0][0].book([0], a)
t[0][0][0].book([1], b)

seat = t[0][0][0]


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
                      command=lambda:main_frame.quit(), height=btn_height, width=btn_width)

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

        wagon_frames.append(wagon_frame)
        wagon_frame.grid(column=tindex, row=1)
        a.grid(column=tindex, row=0)

    btn_book.grid()
    btn_cancel.grid()
    btn_get_ticket.grid()
    btn_exit.grid()
    main_frame.grid(column=0, row=0)
    train_frame.grid(column=1, row=0)
    t.change_button_states("disabled")
    main_root.mainloop()


main_menu()
