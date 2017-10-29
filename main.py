if __name__ == '__main__':
    from lib.train.train import Train
    from lib.booking.schedule import Schedule
    from lib.booking.destination import Destination
    from lib.train.seat import Seat
    from lib.occupant import Person
    from lib.train.wagon import Wagon

    ob = Schedule()
    ob.add_destination(Destination("Fjollträsk"))
    ob.add_destination(Destination("Mesberg"))
    ob.add_destination(Destination("Sumptuna"))
    # w = Wagon(1, 4, 5)
    # w.print()
    t = Train()
    t.add_wagon(Wagon(1, 4, 5))
    t.add_wagon(Wagon(2, 2, 10))
    t.set_schedule(ob)
    a = Person("Sven")
    t[0][0][0].book([0,1],a)
    t.print_nice(lambda x : x.seat_is_booked([0]))
    t.print_nice(lambda x : x.seat_is_booked([1]))
    s = Seat(1)
    s.set_schedule(ob)
    s.book([0, 1], a)
    s.get_schedule.print()
