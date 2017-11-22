from lib.booking.TicketPart import CompleteTicket
from lib.train.BaseTrain import BaseTrain, ErrorInFile
from lib.train.seat import Walkway


class Train(BaseTrain):
    """The Main container for a train."""

    def book_number(self, schedule_index, number_of_seats, occupant, allow_separation=False):
        """Books a set number of seat."""
        return super(Train, self).book_number(schedule_index, number_of_seats, occupant, allow_separation)

    def __init__(self, train_name):
        """Sets the name for the train and creates attributes __schedule and __wagon for later use"""
        super(Train, self).__init__()
        self.__wagons = []
        self.__schedule = None
        self.__name = train_name

    def __iter__(self):
        """Iterates over its wagons."""
        for i in self.__wagons:
            yield i

    def __getitem__(self, item):
        """returns corresponding item from __wagons"""
        return self.__wagons[item]

    def get_name(self):
        """Returns its names"""
        return self.__name

    def get_wagons(self):
        """returns wagon list"""
        return self.__wagons

    def get_schedule(self):
        """returns its schedule."""
        return self.__schedule

    def get_max_length_travel(self):
        """Calls max_schedule_index() from schedule"""
        return self.__schedule.max_schedule_index()

    def set_schedule(self, schedule):

        self.__schedule = schedule
        super(Train, self).set_schedule(schedule)

    def get_bookings(self, occupant):
        """returns all bookings for a occupant as a CompleteTicket object"""
        bookings = []
        for wagon in self.__wagons:
            temp_tickets = wagon.get_bookings(occupant)
            if temp_tickets is not None:
                bookings.extend(temp_tickets)
        if len(bookings) <= 0:
            return
        ticket = CompleteTicket(bookings)
        return ticket

    @classmethod
    def read_from_file(cls, et):
        """This is for the recreation of a train from xml format.
        First fetches schedule because all seats need it for their setup"""
        try:
            t = Train(et.attrib["name"])
            from lib.booking.schedule import Schedule
            t.set_schedule(Schedule.read_from_file(et))
            from lib.train.wagon import Wagon
            for i in et.find("wagons"):
                w = Wagon.read_from_file(i, t)
                w.set_parent(t)
                t.add_wagon(w)
            return t
        except KeyError:
            print("faulty file.")
            raise ErrorInFile("An error is in the file. Cant read.")

    def get_as_element(self,et= None):
        """Is used for getting the train in xml.etree.ElementTree format.
        First sets it own attrib and the run corresponding in all wagons"""
        import xml.etree.ElementTree as et
        train = et.Element("train", attrib={"name": self.__name})
        train.append(self.__schedule.get_as_element())
        w = et.SubElement(train, "wagons")
        for wagon in self.__wagons:
            w.append(wagon.get_as_element())
        return train

    def add_wagon(self, wagon):
        """Adds wagon to its list."""
        self.__wagons.append(wagon)

    def print_nice(self, predicate):
        """Prints a nice train in the console."""
        wagons = []
        print("Train: {0}".format(self.__name))
        for wagon in self.__wagons:
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

        print("Train: {}".format(self.__name))
        destination_string = []
        for i in range(self.__schedule.__len__()):
            destination_string.append("#{1:1} {0}".format(self.__schedule[i].name, i + 1))
        print("\n".join(destination_string))
        for wagon in self.__wagons:
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

    def window_header_display(self):
        """Is Called for the window title"""
        return "Train: {0}. Traveling: {1}".format(self.get_name(), self.get_schedule().get_destination_chain())

    def summary_display(self, occupant=None):
        """Generats string for shortly displaying all tickets for occupant and general train information."""
        text = "Train: {0}\nDeparting @{3}\n{2} Free seats\n{1}".format(self.get_name(),
                                                                        self.get_schedule().get_destination_chain(),
                                                                        self.get_number_of_free_seats(
                                                                            self.get_max_length_travel()),
                                                                        self.__schedule.get_departure_time())
        occupant_tickets = self.get_bookings(occupant)
        if occupant_tickets is not None:
            text += "\n{0}{1}{0}".format("-" * 11, "Tickets")
            text += "\n" + occupant_tickets.destination_list()
        else:
            text += "\n" + "-" * 30
        return text

    def train_table_display(self):
        """special function for MainMenu to get a different formatted string to display."""
        return "{0}".format(self.__name)
