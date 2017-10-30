from tkinter import *

from lib.booking.destination import Destination
from lib.booking.schedule import Schedule
from lib.occupant import Person
from lib.train.train import Train
from lib.train.wagon import Wagon

t = Train("X8000")
t.add_wagon(Wagon(1, 4, 5))
t.add_wagon(Wagon(2, 4, 10))
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


def main_menu():
    def print_num(*args):
        #rint(seat.get_seat_number())
        btn_text.set(btn_text.get() + "a")

    main_root = Tk()
    main_frame = Frame(main_root)

    btn_text = StringVar()
    btn_text.set("A")

    seat = t[0][0][0]

    button = Button(main_frame, textvariable=btn_text,
                    command=seat.print_formatted, height=2, width=20)
    main_frame.pack()
    button.pack()
    main_root.mainloop()


main_menu()
