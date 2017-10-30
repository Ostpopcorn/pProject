from lib.train.seat import Walkway


class Train(object):
    def __init__(self, train_name):
        self.wagons = []
        self.schedule = None
        self.name = train_name

    def add_wagon(self, wagon):
        self.wagons.append(wagon)

    def set_schedule(self, schedule):
        self.schedule = schedule
        for wagon in self.wagons:
            wagon.set_schedule(schedule)

    def get_bookings(self, occupant):
        bookings = []
        for wagon in self.wagons:
            bookings.extend(wagon.get_bookings(occupant))
        return bookings

    def print_nice_2(self,predicate, horizontal=True):
        wagons = []
        print("Train: {0}".format(self.name))
        for wagon in self.wagons:
            wagons.append(wagon.print_array_formatted(predicate))
        for line in range(wagons[0].__len__()):
            for wagon in wagons:
                if wagon.__len__() > line:
                    if isinstance(wagon[line], list):
                        print("".join(wagon[line]), end="")
                    else:
                        print(wagon[line], end="")
                    print("  ", end="")
            print("")

    def print_nice(self, predicate):

        print("Train: {}".format(self.name))
        destination_string = []
        for i in range(self.schedule.__len__()):
            destination_string.append("#{1:1} {0}".format(self.schedule[i].name, i + 1))
        print("\n".join(destination_string))
        for wagon in self.wagons:
            print("")
            print(" Wagon #{}".format(wagon.get_wagon_number()))
            for seat_column in range(wagon.seats_per_row + 1):
                print("  |", end="")
                for row in wagon.rows:
                    # print("{0:3}".format(row[seat_column].get_seat_number()), end="")
                    if isinstance(row[seat_column], Walkway):
                        print("{0:3}".format(""), end="")
                    else:
                        print("{0:3}".format(predicate(row[seat_column])), end="")
                print("|", end="")
                print("")

    def __getitem__(self, item):
        return self.wagons[0]
