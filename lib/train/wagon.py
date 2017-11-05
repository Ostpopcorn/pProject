from lib.train.row import Row


class Wagon(object):
    @classmethod
    def read_from_file(cls, et,train):
        w = Wagon(int(et.attrib["name"]))
        for i in et.findall("row"):
            r = Row.read_from_file(i,train)
            r.set_parent(w)
            w.add_row(r)

        return w

    @classmethod
    def generate(cls, wagon_number, number_of_seats_per_row, number_of_rows, walkway_index=-1):
        w = Wagon(wagon_number)
        for i in range(number_of_rows):
            w.add_row(Row.generate(w, number_of_seats_per_row, walkway_index
                                   , 1 + (number_of_seats_per_row * i), i))
        return w

    def add_row(self, row):
        self.__rows.append(row)

    def set_parent(self, item):
        if self.__parent is None:
            self.__parent = item
            return
        raise AttributeError("Parent is already set")

    def get_as_element(self):
        import xml.etree.cElementTree as et
        a = et.Element("wagon", attrib={"name": str(self.__wagon_number)})
        for row in self.__rows:
            a.append(row.get_as_element())
        pass
        return a

    #    def __init__(self,parent, wagon_number, number_of_seats_per_row, number_of_rows, walkway_index=-1):
    #        self.__parent = parent
    #        self.__wagon_number = wagon_number
    #        self.__seats_per_row = number_of_seats_per_row
    #        self.rows = []
    #        for i in range(number_of_rows):
    #            self.rows.append(Row(self,number_of_seats_per_row, walkway_index
    #                                 , 1 + (number_of_seats_per_row * i),i))
    def __init__(self, wagon_number):
        self.__wagon_number = wagon_number
        self.__parent = None
        self.__rows = []
        pass

    def get_parent(self):
        return self.__parent

    def set_button_command(self, predicate):
        for i in self.__rows:
            i.set_button_command(predicate)

    def set_button_text(self, predicate):
        for i in self.__rows:
            i.set_button_text(predicate)

    def change_button_states(self, state):
        for i in self.__rows:
            i.change_button_states(state)

    def set_schedule(self, schedule):
        for row in self.__rows:
            row.set_schedule(schedule)

    def update_buttons(self, schedule_index, occupant):
        for i in self.__rows:
            i.update_buttons(schedule_index, occupant)

    def print_array(self):
        return_list = []
        for i in self.__rows:
            return_list.append(i.print_array())
        return return_list

    def print_array_formatted(self, predicate):
        return_list = [["|"] for _ in range(self.__seats_per_row + 1)]
        for row_index in range(self.__rows.__len__()):
            for seat_index in range(self.__rows[row_index].__len__()):
                from lib.train.seat import Walkway
                if isinstance(self.__rows[row_index][seat_index], Walkway):
                    return_list[seat_index].append("{0:3}".format(""))
                    continue
                return_list[seat_index].append("{0:3}".format(predicate(self.__rows[row_index][seat_index])))
        for i in range(self.__seats_per_row + 1):
            return_list[i] += "|"

        return_list.insert(0, " " + "-" * (self.__rows.__len__() * 3) + " ")
        return_list.insert(0, (" Wagon #{0:<" + str(self.__rows.__len__() * 3 - 6) + "}").format(self.__wagon_number))
        return_list.append(" " + "-" * (self.__rows.__len__() * 3) + " ")
        return return_list

    def print(self):
        for i in self.__rows:
            print(" , ".join(i.print_array()))

    def get_wagon_number(self):
        return self.__wagon_number

    def get_bookings(self, occupant):
        bookings = []
        for row in self.__rows:
            bookings.extend(row.get_bookings(occupant))
        return bookings

    def __getitem__(self, item):
        return self.__rows[item]

    def __len__(self):
        return self.__rows.__len__()


if __name__ == '__main__':
    ob = Wagon(1, 6, 7, 3)
    ob.print()
