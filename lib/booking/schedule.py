from lib.booking.destination import Destination


class Schedule(object):
    def __init__(self):
        self.__destinations = []

    def add_destination(self,destination):
        if not issubclass(destination,Destination):
            raise ValueError("Is not of type" + Destination.__name__)
        self.__destinations.append(destination)