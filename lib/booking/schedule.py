from lib.booking.destination import Destination


class Schedule(object):
    def __init__(self):
        self.__destinations = []

    def add_destination(self, destination):
        if not isinstance(destination, Destination):
            raise ValueError("Is not of type" + Destination.__name__)
        self.__destinations.append(destination)

    def number_of_stops(self):
        return self.__destinations.__len__()

    def __len__(self):
        return self.number_of_stops()

    def __getitem__(self, item):
        return self.__destinations[item]


class Ticket(object):
    def __init__(self, a, b, occupant):
        self.occupant = occupant
        self.destination = b
        self.start = a


class SeatSchedule(object):
    def __init__(self, wagon_schedule):
        self.master_schedule = wagon_schedule
        self.__bookings = [None for _ in range(self.master_schedule.number_of_stops() - 1)]

    def book(self, schedule_index, occupant):
        self.__bookings[schedule_index] = Ticket(self.master_schedule[schedule_index]
                                                 , self.master_schedule[schedule_index + 1],occupant)

    def print(self):
        for i in range(self.__bookings.__len__()):
            print(self.master_schedule[i].name, self.master_schedule[i + 1].name)
            print("   ", self.__bookings[i])
