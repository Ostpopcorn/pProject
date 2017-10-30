from lib.train.row import Row


class Wagon(object):
    def __init__(self, wagon_number, number_of_seats_per_row, number_of_rows, walkway_index=-1):
        self.__wagon_number = wagon_number
        self.seats_per_row = number_of_seats_per_row
        self.rows = []
        for i in range(number_of_rows):
            self.rows.append(Row(number_of_seats_per_row, walkway_index
                                 , 1 + (number_of_seats_per_row * i)))

    def set_schedule(self, schedule):
        for row in self.rows:
            row.set_schedule(schedule)

    def print_array(self):
        return_list = []
        for i in self.rows:
            return_list.append(i.print_array())
        return return_list

    def print_array_formatted(self,predicate):
        return_list = [["|"] for _ in range(self.seats_per_row + 1)]
        for row_index in range(self.rows.__len__()):
            for seat_index in range(self.rows[row_index].__len__()):
                from lib.train.seat import Walkway
                if isinstance(self.rows[row_index][seat_index],Walkway):
                    return_list[seat_index].append("{0:3}".format(""))
                    continue
                return_list[seat_index].append("{0:3}".format(predicate(self.rows[row_index][seat_index])))
        for i in range(self.seats_per_row + 1):
            return_list[i] += "|"

        return_list.insert(0, " " + "-"* (self.rows.__len__()*3)+ " ")
        return_list.insert(0, (" Wagon #{0:<"+str(self.rows.__len__()*3-6)+ "}").format(self.__wagon_number))
        return_list.append(" " + "-"* (self.rows.__len__()*3)+ " ")
        return return_list

    def print(self):
        for i in self.rows:
            print(" , ".join(i.print_array()))

    def get_wagon_number(self):
        return self.__wagon_number

    def get_bookings(self, occupant):
        bookings = []
        for row in self.rows:
            bookings.extend(row.get_bookings(occupant))
        return bookings

    def __getitem__(self, item):
        return self.rows[0]


if __name__ == '__main__':
    ob = Wagon(1, 6, 7, 3)
    ob.print()
