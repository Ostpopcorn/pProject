from lib.train.BaseTrain import BaseTrain
from lib.train.row import Row


class Wagon(BaseTrain):
    """Contains row and is meant to be contained in Train."""

    def book_number(self, schedule_index, number_of_seats, occupant, allow_separation):
        booked = super(Wagon, self).book_number(schedule_index, number_of_seats, occupant,allow_separation)

        return booked

    def __iter__(self):
        for i in self.__rows:
            yield i

    @classmethod
    def generate(cls, wagon_number, number_of_seats_per_row, number_of_rows, walkway_index=-1):
        """Generates a fresh Wagon based on numbers"""
        w = Wagon(wagon_number)
        for i in range(number_of_rows):
            w.add_row(Row.generate(w, number_of_seats_per_row, walkway_index
                                   , 1 + (number_of_seats_per_row * i), i))
        return w

    def __init__(self, wagon_number):
        """sets a given wagon_number and creates __parent and __rows"""
        self.__wagon_number = wagon_number
        BaseTrain.__init__(self)
        self.__rows = []
        pass

    def __getitem__(self, item):
        """returns corresponding item from __rows"""
        return self.__rows[item]

    def __len__(self):
        """returns the len of __rows """
        return self.__rows.__len__()

    def add_row(self, row):
        self.__rows.append(row)

    def get_wagon_number(self):
        return self.__wagon_number

    def get_as_element(self):
        """Is used for getting the train in xml.etree.ElementTree format.
        First sets it own attrib and the run corresponding in all rows"""
        import xml.etree.cElementTree as et
        a = et.Element("wagon", attrib={"name": str(self.__wagon_number)})
        for row in self.__rows:
            a.append(row.get_as_element())
        pass
        return a

    @classmethod
    def read_from_file(cls, et, train):
        """This is for the recreation of a train from xml format."""
        w = Wagon(int(et.attrib["name"]))
        for i in et.findall("row"):
            r = Row.read_from_file(i, train)
            r.set_parent(w)
            w.add_row(r)

        return w

    def print_array(self):
        """returns the class as an array for easier printing later"""
        return_list = []
        for i in self.__rows:
            return_list.append(i.print_array())
        return return_list

    def print_array_formatted(self, predicate):
        """returns a fully formatted array with strings for printing later"""
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


if __name__ == '__main__':
    pass
