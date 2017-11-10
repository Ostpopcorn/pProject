class BaseTrain(object):
    def __init__(self):
        self.__parent = None

    def __is_seat(self):
        from lib.train.seat import Seat
        return isinstance(self,Seat)


    @staticmethod
    def correct_index_format(schedule_index):
        new_index = ""
        if not isinstance(schedule_index, list):
            new_index = [new_index]
        else:
            new_index = schedule_index
        for i in new_index:
            if not isinstance(i, int):
                raise ValueError("Expected type int")
        return new_index

    def __iter__(self):
        raise NotImplementedError("Fett kul")

    def get_number_of_free_seats(self, schedule_index):
        from lib.train.seat import Seat
        if self.__is_seat():
            if self.is_booked(schedule_index):
                return 0
            return 1
        else:
            number_of_free_seats = 0
            for row in self:
                number_of_free_seats += row.get_number_of_free_seats(schedule_index)
            return number_of_free_seats

    def set_parent(self, item):
        """sets parent, hopefully its Train.
        Only allows setting once"""
        if self.__parent is None:
            self.__parent = item
            return
        raise AttributeError("Parent is already set")

    def get_parent(self):
        return self.__parent

    def set_button_command(self, predicate):
        for i in self:
            i.set_button_command(predicate)

    def set_button_text(self, predicate):
        for i in self:
            i.set_button_text(predicate)

    def change_button_states(self, state):
        for i in self:
            i.change_button_states(state)

    def set_schedule(self, schedule):
        for row in self:
            row.set_schedule(schedule)

    def update_buttons(self, schedule_index, occupant):
        for i in self:
            i.update_buttons(schedule_index, occupant)

    def get_bookings(self, occupant):
        from lib.booking.TicketPart import SeatTicket
        bookings = None
        for seat in self:
            temp_list = seat.get_bookings(occupant)
            if temp_list is not None:
                if bookings is None:
                    bookings = []
                if isinstance(temp_list, list):
                    bookings.extend(temp_list)
                elif isinstance(temp_list, SeatTicket):
                    bookings.append(temp_list)
                else:
                    raise ValueError("wierdo")
        return bookings
