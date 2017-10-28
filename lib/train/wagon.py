from lib.train.row import Row


class Wagon(object):
    def __init__(self, wagon_number, number_of_seats_per_row, number_of_rows, walkway_index=-1):
        self.wagon_number = wagon_number
        self.rows = []
        for i in range(number_of_rows):
            self.rows.append(Row(number_of_seats_per_row, walkway_index
                                 , 1 + (number_of_seats_per_row * i)))

    def print(self):
        for i in self.rows:
            print(" , ".join(i.print_array()))


if __name__ == '__main__':
    ob = Wagon(1, 6, 7, 3)
    ob.print()
