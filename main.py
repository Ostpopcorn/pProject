import os

from lib.interaction.MainMenu import MainMenu
import xml.etree.ElementTree as et
from lib.train.train import Train


def generate_new_trains(root):
    from lib.train.wagon import Wagon
    from lib.booking.schedule import Schedule
    from lib.booking.destination import Destination

    ob = Schedule()
    ob.add_destination(Destination("Öteborg"))
    ob.add_destination(Destination("Tockholm"))
    t = Train("MTR Egg-press")
    w = Wagon.generate(1, 4, 6)
    w.set_parent(t)
    t.add_wagon(w)
    w = Wagon.generate(2, 4, 6)
    w.set_parent(t)
    t.add_wagon(w)
    w = Wagon.generate(3, 4, 6)
    w.set_parent(t)
    t.add_wagon(w)
    t.set_schedule(ob)

    t1 = t
    ob = Schedule()
    ob.add_destination(Destination("Fjollträsk"))
    ob.add_destination(Destination("Mesberg"))
    ob.add_destination(Destination("Sumptuna"))
    t = Train("X2000")
    w = Wagon.generate(1, 6, 5)
    w.set_parent(t)
    t.add_wagon(w)
    w = Wagon.generate(2, 4, 10)
    w.set_parent(t)
    t.add_wagon(w)
    t.set_schedule(ob)

    t2 = t

    ob = Schedule()
    ob.add_destination(Destination("Tockholm"))
    ob.add_destination(Destination("Tödertälje"))
    ob.add_destination(Destination("Sörping"))
    t = Train("Snälltåget")
    w = Wagon.generate(1, 4, 6)
    w.set_parent(t)
    t.add_wagon(w)
    w = Wagon.generate(2, 4, 6)
    w.set_parent(t)
    t.add_wagon(w)
    w = Wagon.generate(3, 4, 6)
    w.set_parent(t)
    t.add_wagon(w)
    t.set_schedule(ob)

    root.append(t2.get_as_element())
    root.append(t1.get_as_element())
    root.append(t.get_as_element())


if __name__ == '__main__':

    a_path = os.path.abspath(os.path.join("lib", "storage", "a.xml"))
    generate_new = False
    if generate_new:
        root = et.Element("root")
        generate_new_trains(root)
        f = et.ElementTree(root)
    else:
        f = et.parse(a_path)

    main_menu = MainMenu()
    train_list = []
    for i in f.getroot():
        temp_train = Train.read_from_file(i)
        train_list.append(temp_train)
        main_menu.add_train(temp_train)

    main_menu.start_ui()
    e = et.Element("root")

    for i in train_list:
        e.append(i.get_as_element())

    f = et.ElementTree(e)

    f.write(a_path, encoding="utf-8")
