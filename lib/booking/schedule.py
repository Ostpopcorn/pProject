from lib.booking.TicketPart import TicketPart
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

    def print_array_formatted(self):
        for i in range(self.__destinations.__len__()):
            print("#{1}: {0}".format(self.__destinations[i].name, i + 1))
            if i + 1 < self.__destinations.__len__():
                # All but last round
                print("  -Travel time: {0}, Distance {1}".format("unknown", "-1"))
                # else:
                # last loop
                # print("k")


class SeatSchedule(object):
    def __init__(self, wagon_schedule):
        self.master_schedule = wagon_schedule
        self.__bookings = [None for _ in range(self.master_schedule.number_of_stops() - 1)]

    def book(self, schedule_index, occupant):
        self.__bookings[schedule_index] = TicketPart(self.master_schedule[schedule_index]
                                                     , self.master_schedule[schedule_index + 1], occupant)

    def is_booked(self, schedule_index):
        if not isinstance(schedule_index, list):
            schedule_index = [schedule_index]

        for i in schedule_index:
            if self.__bookings[i] is not None:
                return True
        return False

    def print(self):
        for i in range(self.__bookings.__len__()):
            print(self.master_schedule[i].name, self.master_schedule[i + 1].name)
            print("   ", self.__bookings[i])

    def print_array_formatted(self):
        for i in range(self.master_schedule.number_of_stops()):
            print("#{1}: {0}".format(self.master_schedule[i].name, i + 1))
            if i + 1 < self.master_schedule.number_of_stops():
                # All but last round
                if not self.__bookings[i] is None:
                    print("  -Booked by: {0}".format(self.__bookings[i].occupant.name))

    def get_bookings(self, occupant):
        bookings = []
        for booking in self.__bookings:
            if booking is None:
                continue
            if booking.occupant is occupant:
                bookings.append(booking)
        return bookings
