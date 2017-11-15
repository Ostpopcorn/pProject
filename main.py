from lib.train.seat import Seat

if __name__ == '__main__':
    from lib.train.train import Train
    from lib.booking.schedule import Schedule
    from lib.booking.destination import Destination
    from lib.occupant import Person
    from lib.train.wagon import Wagon

    ob = Schedule()
    ob.add_destination(Destination("Fjollträsk"))
    ob.add_destination(Destination("Mesberg"))
    ob.add_destination(Destination("Sumptuna"))
    # ob.print_array_formatted()
    # w = Wagon(1, 4, 5)
    # w.print()
    t = Train("X8000")
    t.add_wagon(Wagon(1, 4, 5))
    t.add_wagon(Wagon(2, 4, 10))
    t.set_schedule(ob)

    # t.print_nice_2()
    a = Person("Sven")
    b = Person("Sverker")
    # t[0][0][0].book([0, 1], a)
    t.print_nice_2(lambda x: x.seat_is_booked([0,1]))
    t[0][0][0].book([0], a)
    t[0][0][1].book([1], b)

    t.print_nice_2(lambda x: x.seat_is_booked([0,1]))
    # t.print_nice_2(lambda x: x.get_seat_number())
    # single_train_interaction(t)
    # t.print_nice(lambda x : x.seat_is_booked([1]))
    t.get_bookings(a).print_formatted()
    # t[0][0][1].print_formatted()
    s = Seat(1)
    s.set_schedule(ob)
    s.book([0, 1], a)
    # s.get_schedule.print_array_formatted()
