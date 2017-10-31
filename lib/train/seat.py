from lib.booking.schedule import SeatSchedule


class Seat(object):
    def __init__(self, seat_number):
        self.__seat_number = seat_number
        self.__schedule = None
        self.__button = None

    def set_button_text(self,predicate):
        if self.button is None:
            print("no button assigned")
            return
        self.button["text"] = predicate(self)

    def set_button(self,button):
        self.__button = button

    def change_button_state(self, state):
        self.__button['state'] = state

    def get_seat_number(self):
        return self.__seat_number

    @property
    def get_schedule(self):
        return self.__schedule

    def set_schedule(self, schedule):
        self.__schedule = SeatSchedule(schedule)

    def is_booked(self, schedule_index):

        return self.get_schedule.is_booked(schedule_index)

    def book(self, schedule_index, occupant):
        if self.__schedule is None:
            raise Exception("No schedule in seat")

        if not isinstance(schedule_index, list):
            schedule_index = [schedule_index]

        for index in schedule_index:
            if isinstance(index, int):
                self.__schedule.book(index, occupant)
            else:
                raise TypeError("expected int for index.")

    def get_bookings(self, occupant):

        return self.__schedule.get_bookings(occupant)

    def print_formatted(self):
        print("Seat: {0}".format(self.get_seat_number()))
        self.__schedule.print_array_formatted()


class Walkway(Seat):
    def __init__(self):
        super(Walkway, self).__init__(-1)

    def is_booked(self, schedule_index):
        return False

    def get_bookings(self, occupant):
        return False
