class TicketPart(object):
    def __init__(self, a, b, occupant):
        self.occupant = occupant
        self.destination = b
        self.start = a

    def print_array(self):
        a = [self.start.name, self.destination.name, self.occupant.full_name()]
        return a

    def __str__(self):
        return "{0} to {1}. {2} as traveler".format(self.start.name, self.destination.name, self.occupant.full_name())


class CompleteTicket(object):
    def __init__(self, ticket_parts):
        self.tickets = ticket_parts

    def print_formatted(self):
        number_of_dashes = 10
        print("-" * number_of_dashes)
        print("Ticket: ")
        for i in self.tickets:
            print(str(i))
        print("-" * number_of_dashes)

    def __str__(self):
        rstring = ""
        for i in self.tickets:
            rstring += str(i) + "\n"
        return rstring
