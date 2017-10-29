from lib.booking.schedule import SeatSchedule


class Seat(object):
    def __init__(self, seat_number):
        self.__seat_number = seat_number
        self.__schedule = None

    def get_seat_number(self):
        return self.__seat_number

    @property
    def get_schedule(self):
        return self.__schedule

    def set_schedule(self, schedule):
        self.__schedule = SeatSchedule(schedule)

    def seat_is_booked(self, schedule_index):

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


class Walkway(Seat):
    def __init__(self):
        super(Walkway, self).__init__(-1)

    def seat_is_booked(self, schedule_index):
        return False

    def get_bookings(self, occupant):
        return False
