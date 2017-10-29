class Train(object):
    def __init__(self):
        self.wagons = []
        self.schedule = None

    def add_wagon(self, wagon):
        self.wagons.append(wagon)

    def set_schedule(self, schedule):
        self.schedule = schedule
        for wagon in self.wagons:
            wagon.set_schedule(schedule)

    def print_nice(self, predicate):
        printrows = []
        for wagon in self.wagons:
            print("")
            for seat_column in range(wagon.seats_per_row + 1):
                print("  |", end="")
                for row in wagon.rows:
                    # print("{0:3d}".format(row[seat_column].get_seat_number()), end="")
                    print("{0:3d}".format(predicate(row[seat_column])), end="")
                print("|", end="")
                print("")

    def __getitem__(self, item):
        return self.wagons[0]
