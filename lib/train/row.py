from lib.train.seat import Seat, Walkway


class Row(object):
    def __init__(self, number_of_seats, walkway_index=-1, start_number=1):
        self.__seats = [Seat(start_number + i) for i in range(number_of_seats)]
        if walkway_index == -1:
            walkway_index = number_of_seats // 2
        else:
            if walkway_index > number_of_seats:
                raise IndexError("walkway is outside the row")
        self.walkway_index = walkway_index


    def set_button_text(self,predicate):
        for i in self.__seats:
            i.set_button_text(predicate)

    def set_button_command(self,predicate):
        for i in self.__seats:
            i.set_button_command(predicate)

    def change_button_states(self, state):
        for i in self.__seats:
            i.change_button_state(state)

    def update_buttons(self,schedule_index,occupant):
        for i in self.__seats:
            i.update_button(schedule_index,occupant)

    def set_schedule(self, schedule):
        for seat in self.__seats:
            seat.set_schedule(schedule)

    def print_array(self):
        return_array = []
        for i in range(0, self.walkway_index):
            return_array.append("{0:2d}".format(self.__seats[i].get_seat_number()))
        return_array.append("W")
        for i in range(self.walkway_index, self.__seats.__len__()):
            return_array.append("{0:2d}".format(self.__seats[i].get_seat_number()))
        return return_array

    def __len__(self):
        return self.__seats.__len__() + 1

    def __getitem__(self, item):
        if item == self.walkway_index:
            return Walkway()
        if item > self.walkway_index:
            return self.__seats[item - 1]
        return self.__seats[item]

    def get_bookings(self, occupant):
        bookings = []
        for seat in self.__seats:
            bookings.extend(seat.get_bookings(occupant))
        return bookings


if __name__ == '__main__':
    ob = Row(4, 2)
    ob.print()
