import os

from lib.train.seat import Seat

if __name__ == '__main__':
    from lib.train.train import Train
    from lib.booking.schedule import Schedule
    from lib.booking.destination import Destination
    from lib.interaction.console import single_train_interaction
    from lib.occupant import Person
    import xml.etree.ElementTree as et
    from lib.train.wagon import Wagon

    ob = Schedule()
    ob.add_destination(Destination("Fjollträsk"))
    ob.add_destination(Destination("Mesberg"))
    ob.add_destination(Destination("Sumptuna"))
    # ob.print_array_formatted()
    # w = Wagon(1, 4, 5)
    # w.print()
    t = Train("X4000")
    w = Wagon.generate(1, 4, 5)
    w.set_parent(t)
    t.add_wagon(w)
    w = Wagon.generate(2, 4, 10)
    w.set_parent(t)
    t.add_wagon(w)

    t.set_schedule(ob)

    b = Person(1234, "Sverker")
    t[0][0][0].book([0, 1], b)

    a_path = os.path.abspath(os.path.join("lib", "storage", "a.xml"))
    root = et.Element("root")
    e = et.ElementTree(root)
    #root.append(t.get_as_element())
    # e.write(a_path)
    #e = et.parse(a_path)
    f = et.parse(a_path)
    for i in f.getroot():
        a = Train.read_from_file(i)
    from lib.interaction.gui import TrainWindow

    tw =TrainWindow(a,Person(1234,"sven"),[0])
    tw.display()
    root2 = et.Element("root")
    root2.append(a.get_as_element())
    f = et.ElementTree(root2)
    root2.append(a.get_as_element())
    f.write(a_path)
    # t.print_nice_2()
    # a = Person("Sven")
    # b = Person("Sverker")
    # t[0][0][0].book([0, 1], a)
    # a =  (t[3])
    # t[0][0][1].book([0], a)
    # t[0][0][1].book([1], b)
    # t.print_nice_2(lambda x: x.seat_is_booked([0]))
    # single_train_interaction(t)
    # t.print_nice(lambda x : x.seat_is_booked([1]))
    # t.get_bookings(a).print_formatted()
    # t[0][0][1].print_formatted()
    # s = Seat(1)
    # s.set_schedule(ob)
    # s.book([0, 1], a)
    # s.get_schedule.print_array_formatted()
