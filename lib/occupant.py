class Occupant(object):
    """The class Seat want to keep as its traveler. Got a ID for keeping track between runs."""

    def __init__(self, ID):
        if not isinstance(ID, int) :
            raise ValueError("Expected int")
        if ID > 0:
            self.__ID = ID

        self.name = ""
        pass

    def get_ID(self):
        return self.__ID

    def get_as_element(self):
        import xml.etree.cElementTree as et
        a = et.Element("occupant", attrib={"id": str(self.get_ID()), "name": self.name})
        return a

    def __eq__(self, other):
        if isinstance(other, Occupant):
            if other.get_ID() == self.get_ID():
                return True
        return False


class Person(Occupant):
    def __init__(self, ID, name):
        super().__init__(ID)
        self.name = name

    def __str__(self):
        return self.name

    def full_name(self):
        return self.name.capitalize()
