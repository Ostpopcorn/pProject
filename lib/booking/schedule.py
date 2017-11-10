from lib.booking.TicketPart import TicketPart
from lib.booking.destination import Destination


class Schedule(object):
    @classmethod
    def read_from_file(cls, et):
        """Reads from given xml format and creates a Schedule."""
        s = Schedule()
        for d in et.find("schedule").findall("Destination"):
            ds = Destination(d.attrib["name"])
            s.add_destination(ds)
        return s

    def max_schedule_index(self):
        a = []
        for i in range(self.number_of_stops()):
            a.append(i)
        return a

    def get_as_element(self):
        """Gets xml format for storage"""
        import xml.etree.cElementTree as et
        a = et.Element("schedule")
        for seat in self.__destinations:
            a.append(seat.get_as_element())
        pass
        return a

    def __init__(self):
        """just sets a list of Destinations"""
        self.__destinations = []

    def add_destination(self, destination):
        if not isinstance(destination, Destination):
            raise ValueError("Is not of type" + Destination.__name__)
        self.__destinations.append(destination)

    def number_of_stops(self):
        """returns the number of places the train will visit"""
        return self.__destinations.__len__()

    def __len__(self):
        return self.number_of_stops()

    def __getitem__(self, item):
        """gets corresponding item i __destination."""
        return self.__destinations[item]

    def print_array_formatted(self):
        """gets a nicely formatted list for later printing"""
        for i in range(self.__destinations.__len__()):
            print("#{1}: {0}".format(self.__destinations[i].name, i + 1))
            if i + 1 < self.__destinations.__len__():
                # All but last round
                print("  -Travel time: {0}, Distance {1}".format("unknown", "-1"))
                # else:
                # last loop
                # print("k")

    def get_destination_chain(self):
        """gets a string containing all stops with ' - ' between"""
        s = "{} - ".format(self.__destinations[0].name)
        for i in range(1, len(self.__destinations) - 1):
            s += "{} - ".format(self.__destinations[i].name)
        s += "{}".format(self.__destinations[len(self.__destinations) - 1].name)
        return s


class SeatSchedule(object):
    """Keeps __booking alongside a Schedule object."""
    @classmethod
    def read_from_file(cls, et, par_sch):
        s = SeatSchedule(par_sch)
        arr = []
        b = et.find("schedule")
        if b is None:
            return SeatSchedule(par_sch)

        for i in b.findall("ticketpart"):
            arr.append(TicketPart.read_from_file(i))
        s.__bookings = arr
        return s

    def has_any_booking(self):
        """if there is any bookings then it returns True"""
        for i in self.__bookings:
            if i is not None:
                return True
        return False

    def get_as_element(self):
        import xml.etree.cElementTree as et
        a = et.Element("schedule")
        for book in self.__bookings:
            if book is not None:
                a.append(book.get_as_element())
            else:
                a.append(et.Element("ticketpart"))
        return a

    def __init__(self, wagon_schedule):
        self.master_schedule = wagon_schedule
        self.__bookings = [None for _ in range(self.master_schedule.number_of_stops() - 1)]

    def book(self, schedule_index, occupant):
        """Generates a TicketPart from destinations corresponding to schedule index and places in __bookings """
        self.__bookings[schedule_index] = TicketPart(self.master_schedule[schedule_index]
                                                     , self.master_schedule[schedule_index + 1], occupant)

    def is_booked(self, schedule_index):
        """returns True if there is a booking in the given indexes"""
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

    def get_destination_chain(self):
        """gets a string containing all stops with ' - ' between"""
        s = "{} - ".format(self.master_schedule[0].start.name)
        for i in range(len(self.master_schedule) - 1):
            s += "{} - ".format(self.master_schedule[i].destination.name)
        s += "{}".format(self.master_schedule[len(self.master_schedule) - 1].destination.name)
        return s

    def print_array_formatted(self):
        """gets a nicely formatted array for later printing"""
        for i in range(self.master_schedule.number_of_stops()):
            print("#{1}: {0}".format(self.master_schedule[i].name, i + 1))
            if i + 1 < self.master_schedule.number_of_stops():
                # All but last round
                if not self.__bookings[i] is None:
                    print("  -Booked by: {0}".format(self.__bookings[i].occupant.name))

    def get_occupant(self, schedule_index):
        """gets occupant in the given schedule indexes"""
        try:
            return self.__bookings[schedule_index].occupant
        except AttributeError:
            return

    def cancel_book(self, schedule_index):
        """removes bookings"""
        self.__bookings[schedule_index] = None

    def get_bookings(self, occupant):
        """gets all bookings for a occupant"""
        bookings = []
        if occupant is None:
            return bookings
        for booking in self.__bookings:
            if booking is None:
                continue
            if booking.occupant.get_ID() == occupant.get_ID():
                bookings.append(booking)
        return bookings
