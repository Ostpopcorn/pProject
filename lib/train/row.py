from lib.train.seat import Seat, Walkway


class Row(object):
    """Contains a array of seats. Functions mostly as a list with special functions"""
    @classmethod
    def read_from_file(cls, et,train):
        """This is for the recreation of a train from xml format."""
        r = Row(int(et.attrib["name"]))
        r.__walkway_index = int(et.attrib["walkway_index"])
        for i in et.findall("seat"):
            s = Seat.read_from_file(i,train)
            s.set_parent(r)
            r.add_seat(s)
        return r

    @classmethod
    def generate(cls, parent, number_of_seats, walkway_index=-1, start_number=1, index=-1):
        """Generates a fresh Wagon based on numbers"""
        r = Row(index)
        r.set_parent(parent)
        for i in range(number_of_seats):
            s = Seat(start_number + i)
            s.set_parent(r)
            r.add_seat(s)

        if walkway_index == -1:
            walkway_index = number_of_seats // 2
        else:
            if walkway_index > number_of_seats:
                raise IndexError("walkway is outside the row")
        r.__walkway_index = walkway_index
        return r

    def add_seat(self, seat):
        self.__seats.append(seat)

    def get_as_element(self):
        """Is used for getting the train in xml.etree.ElementTree format.
        First sets it own attrib and the run corresponding in all seats"""
        import xml.etree.cElementTree as et
        a = et.Element("row", attrib={"name": str(self.__index),
                                      "walkway_index": str(self.__walkway_index)})
        for seat in self.__seats:
            a.append(seat.get_as_element())
        pass
        return a

    def set_walkway_index(self, walkway_index):
        if walkway_index == -1:
            self.__walkway_index = int(walkway_index)
            return
        raise ValueError("walkway_index already set")


    def __init__(self, index):
        self.__index = index
        self.__parent = None
        self.__seats = []
        self.__walkway_index = -1

    def get_parent(self):
        return self.__parent

    def set_parent(self, item):
        if self.__parent is None:
            self.__parent = item
            return
        raise AttributeError("Parent is already set")

    def set_button_text(self, predicate):
        for i in self.__seats:
            i.set_button_text(predicate)

    def set_button_command(self, predicate):
        for i in self.__seats:
            i.set_button_command(predicate)

    def change_button_states(self, state):
        for i in self.__seats:
            i.change_button_state(state)

    def update_buttons(self, schedule_index, occupant):
        for i in self.__seats:
            i.update_button(schedule_index, occupant)

    def set_schedule(self, schedule):
        for seat in self.__seats:
            seat.set_schedule(schedule)

    def print_array(self):
        return_array = []
        for i in range(0, self.__walkway_index):
            return_array.append("{0:2d}".format(self.__seats[i].get_seat_number()))
        return_array.append("W")
        for i in range(self.__walkway_index, self.__seats.__len__()):
            return_array.append("{0:2d}".format(self.__seats[i].get_seat_number()))
        return return_array

    def __len__(self):
        return self.__seats.__len__() + 1

    def __getitem__(self, item):
        item = int(item)
        if item == self.__walkway_index:
            return Walkway(self)
        if item > self.__walkway_index:
            return self.__seats[item - 1]
        return self.__seats[item]

    def get_bookings(self, occupant):
        bookings = []
        for seat in self.__seats:
            templist = seat.get_bookings(occupant)
            if templist is not None:
                bookings.append(templist)
        return bookings


if __name__ == '__main__':
    pass
