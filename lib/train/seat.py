from lib.booking.schedule import SeatSchedule
from lib.train.BaseTrain import BaseTrain


class SeatBookedError(Exception):
    """Simple error that is raised when a seat is already booked."""
    def __init__(self, text):
        Exception.__init__(self, text)


class Seat(BaseTrain):
    """The container for a seat in the train."""
    def __iter__(self):
        """Must be implemented to shadow parrent class method."""
        raise AttributeError("Seat is not enumerable")

    @classmethod
    def read_from_file(cls, et, train):
        """This is for the recreation of a train from xml format."""
        s = Seat(et.attrib["number"])

        s.__schedule = SeatSchedule.read_from_file(et, train.get_schedule())

        return s

    def __init__(self, seat_number):
        """Creats variables and calls parent constructor"""
        super().__init__()
        self.__seat_number = seat_number
        self.__schedule = None
        self.__button = None

    def get_as_element(self):
        """Is used for getting the train in xml.etree.ElementTree format.
        First sets it own attrib and then gets its SeatSchedule from file"""
        import xml.etree.cElementTree as et
        a = et.Element("seat", attrib={"number": str(self.__seat_number)})
        if self.__schedule.has_any_booking():
            a.append(self.__schedule.get_as_element())
        return a

    def set_button(self, button):
        """Sets button is set."""
        self.__button = button

    def change_button_states(self, state):
        """Calls change_button_state. Is needed because of parent class."""
        self.change_button_state(state)

    def change_button_state(self, state):
        """Chages its buttons state."""
        self.__button['state'] = state

    def get_seat_number(self):
        """returns seatnumber."""
        return self.__seat_number

    def update_buttons(self, schedule_index, occupant):
        """Calls update_button. Is needed because of parent class."""
        self.update_button(schedule_index, occupant)

    def set_button_command(self, predicate):
        """sets button onclick event."""
        self.__button["command"] = lambda: predicate(self)

    def update_button(self, schedule_index, occupant):
        """updates the color and text of a button so it matches given parameters"""
        if self.__button is None:
            return
        if not isinstance(schedule_index, list):
            schedule_index = [schedule_index]
        if not self.is_booked(schedule_index):
            self.__button["background"] = "white"
        else:
            if self.__schedule.get_bookings(occupant=occupant):
                self.__button["background"] = "pale green"
            else:
                self.__button["background"] = "orange red"
                # self.set_button_text(lambda x:x.is_booked(schedule_index))

    @property
    def get_schedule(self):
        """returns its schedule."""
        return self.__schedule

    def set_schedule(self, schedule):
        """Creates a seatschedule from schedule and sets it to __schedule."""
        self.__schedule = SeatSchedule(schedule)

    def is_booked(self, schedule_index):
        """returns True if a seat is book in at least one of alla indexes given"""
        return self.get_schedule.is_booked(schedule_index)

    def book(self, schedule_index, occupant):
        """books a seat for the given time with the occupant as traveler"""
        if self.__schedule is None:
            raise Exception("No schedule in seat")

        if not isinstance(schedule_index, list):
            schedule_index = [schedule_index]

        for index in schedule_index:
            if isinstance(index, int):
                if self.is_booked(index):
                    if self.__schedule.get_occupant(index).get_ID() == occupant.get_ID():
                        self.__schedule.cancel_book(index)
                    else:  # self.__schedule.get_bookings(occupant).__len__() <= 0:
                        raise SeatBookedError("Seat is already booked")
                else:
                    self.__schedule.book(index, occupant)
            else:
                raise TypeError("expected int for index.")
        self.update_button(schedule_index, occupant)

    def get_bookings(self, occupant):
        """gets all bookings for the occupant as a SeatTicket."""
        ticket_parts = self.__schedule.get_bookings(occupant)
        if ticket_parts.__len__() <= 0:
            return
        from lib.booking.TicketPart import SeatTicket
        ticket = SeatTicket(self)
        for i in ticket_parts:
            ticket.add_ticket_part(i)
        return ticket


class Walkway(Seat):
    """A dummy for marking walkway in the train. Some funtions are overwritten to only return None"""

    def __init__(self, parent):
        """Gives parent a seat number that is unreachable by the rest of the program"""
        super(Walkway, self).__init__(-1)
        self.set_parent(parent)

    def is_booked(self, schedule_index):
        return None

    def get_bookings(self, occupant):
        return None
