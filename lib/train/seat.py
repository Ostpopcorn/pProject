from lib.booking.schedule import SeatSchedule


class Seat(object):
    def __init__(self, seat_number):
        self.__seat_number = seat_number
        self.__schedule = None

    @property
    def get_seat_number(self):
        return self.__seat_number

    @property
    def get_schedule(self):
        return self.__schedule

    def set_schedule(self, schedule):
        self.__schedule = SeatSchedule(schedule)

    def book(self, schedule_index, occupant):
        if not self.__schedule is None:
            self.__schedule.book(schedule_index, occupant)
