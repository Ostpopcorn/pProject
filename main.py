import os

from lib.interaction.MainMenu import MainMenu
from lib.train.seat import Seat

if __name__ == '__main__':
    from lib.train.train import Train
    from lib.booking.schedule import Schedule
    from lib.booking.destination import Destination
    from lib.interaction.console import single_train_interaction
    from lib.occupant import Person
    import xml.etree.ElementTree as et
    from lib.train.wagon import Wagon
    #
    # ob = Schedule()
    # ob.add_destination(Destination("Fjollträsk"))
    # ob.add_destination(Destination("Mesberg"))
    # ob.add_destination(Destination("Sumptuna"))
    # # ob.print_array_formatted()
    # # w = Wagon(1, 4, 5)
    # # w.print()
    # t = Train("X4000")
    # w = Wagon.generate(1, 4, 5)
    # w.set_parent(t)
    # t.add_wagon(w)
    # w = Wagon.generate(2, 4, 10)
    # w.set_parent(t)
    # t.add_wagon(w)
    #
    # t.set_schedule(ob)

    a_path = os.path.abspath(os.path.join("lib", "storage", "a.xml"))
    # root = et.Element("root")
    # e = et.ElementTree(root)
    # root.append(t.get_as_element())
    # e.write(a_path)
    # e = et.parse(a_path)
    f = et.parse(a_path)
    main_menu = MainMenu()
    for i in f.getroot():
        main_menu.add_train(Train.read_from_file(i))

    main_menu.start_ui()
    e = et.Element("root")
    for i in main_menu.get_trains():
        e.append(i.get_as_element())

    f = et.ElementTree(e)

    f.write(a_path,encoding="utf-8")

