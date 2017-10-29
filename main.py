

if __name__ == '__main__':
    from lib.booking.schedule import Schedule
    from lib.booking.destination import Destination
    from lib.train.seat import Seat
    from lib.occupant import Person
    ob = Schedule()
    ob.add_destination(Destination("Fjollträsk"))
    ob.add_destination(Destination("Mesberg"))
    ob.add_destination(Destination("Sumptuna"))
    s = Seat(1)
    s.set_schedule(ob)
    s.book(1, Person("Sven"))
    s.get_schedule.print()