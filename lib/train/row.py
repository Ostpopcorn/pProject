from lib.train.seat import Seat


class Row(object):
    def __init__(self, number_of_seats, walkway_index=-1, start_number = 1):
        self.seats = [Seat(start_number +i) for i in range(number_of_seats)]
        if walkway_index == -1:
            walkway_index = number_of_seats // 2
        else:
            if walkway_index > number_of_seats:
                raise IndexError("walkway is outside the row")
        self.walkway_index = walkway_index

    def print_array(self):
        return_array = []
        for i in range(0, self.walkway_index):
            return_array.append("{0:2d}".format(self.seats[i].seat_number))
        return_array.append("W")
        for i in range(self.walkway_index, self.seats.__len__()):
            return_array.append("{0:2d}".format(self.seats[i].seat_number))
        return return_array

if __name__ == '__main__':
    ob = Row(4, 2)
    ob.print()
