class TicketPart(object):
    """Contains two destinations and a occupant as a ticket."""

    @classmethod
    def read_from_file(cls, et):
        """Reads given elementtree and returns a TicketPart"""
        try:
            s = et.find("start").find("Destination")
            e = et.find("end").find("Destination")
            a = et.find("occupant").attrib
        except AttributeError:
            return

        from lib.occupant import Person
        from lib.booking.destination import Destination
        return TicketPart(Destination.read_from_file(s)
                          , Destination.read_from_file(e)
                          , Person(int(a["id"]), a["name"]))

    def get_as_element(self):
        """Converts itself to a elementtree format"""
        import xml.etree.cElementTree as et
        a = et.Element("ticketpart")
        s = self.start.get_as_element()
        e = self.destination.get_as_element()

        t = et.SubElement(a, "start")
        t.append(s)

        t = et.SubElement(a, "end")
        t.append(e)
        a.append(self.occupant.get_as_element())
        return a

    def __init__(self, a, b, occupant, train=-1, wagon=-1, seat=-1):
        """requires a start, end and an occupant."""
        self.occupant = occupant
        self.destination = b
        self.start = a
        self.train = train
        self.seat = seat
        self.wagon = wagon

    def print_array(self):
        """Returns a array for printing later."""
        a = [self.start.name, self.destination.name, self.occupant.full_name()]
        return a

    def formatted_string(self, include_traveler=True):
        """returns a formatted string for printing"""
        sreturn = "{0} to {1}".format(self.start.name, self.destination.name)
        if include_traveler:
            sreturn += ". {0} as traveler".format(self.occupant.full_name())
        return sreturn

    def __str__(self):
        """returns formatted_string()."""
        return self.formatted_string()


class SeatTicket(object):
    """Is for all tickets for a occupant in one seat."""
    def __init__(self, seat):
        """gets train, wagon based on the seat object"""
        self.__train_name = seat.get_parent().get_parent().get_parent().get_name()
        self.__wagon_number = seat.get_parent().get_parent().get_wagon_number()
        self.__seat_number = seat.get_seat_number()
        self.__ticket_parts = []

    def add_ticket_part(self, ticket_part):
        """Adds ticketpart to its list."""
        if not isinstance(ticket_part, TicketPart):
            raise ValueError("Not a ticket_part")
        self.__ticket_parts.append(ticket_part)

    def __last_ticket_part(self):
        """gets last ticketpart."""
        return self.__ticket_parts[self.__ticket_parts.__len__() - 1]

    def __get_destination_chain(self):
        """Returns a string with all destinations combined with ' - '."""
        s = "{} - ".format(self.__ticket_parts[0].start.name)
        for i in range(len(self.__ticket_parts) - 1):
            s += "{} - ".format(self.__ticket_parts[i].destination.name)
        s += "{}".format(self.__ticket_parts[len(self.__ticket_parts) - 1].destination.name)
        return s

    def mini_display_format(self):
        """display format for gui and ticket display"""
        return "Wagon: {0}. Seat:{1}. \n{2}\n".format(self.__wagon_number, self.__seat_number,
                                                      self.__get_destination_chain())


class CompleteTicket(object):
    """Should contain all tickets for a occupant for one or many trains."""
    def __init__(self, seat_tickets):
        self.__tickets = seat_tickets

    def get_file_string(self):
        """Format for printing to file."""
        a_string = ""
        for i in self.__tickets:
            a_string += i.mini_display_format()
        return a_string

    def destination_list(self):
        """returns all destinations combined with \n"""
        rstring = ""
        for i in self.__tickets:
            rstring += i.mini_display_format() + "\n"
        return rstring

    def print_formatted(self):
        """prints itself in a formatted manor to console"""
        number_of_dashes = 10
        print("-" * number_of_dashes)
        print("Ticket: ")
        for i in self.__tickets:
            print(str(i))
        print("-" * number_of_dashes)

    def __str__(self):
        """returns self.destination_list()"""
        return self.destination_list()

    def __len__(self):
        """returns the length of ticketlist."""
        return self.__tickets.__len__()
