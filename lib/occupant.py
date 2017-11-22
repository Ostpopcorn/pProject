class Occupant(object):
    """The class Seat want to keep as its traveler. Got a ID for keeping track between runs."""

    def __init__(self, ID):
        """BaseClass has id and sets it on creation."""
        if not isinstance(ID, int) :
            raise ValueError("Expected int")
        if ID > 0:
            self.__ID = ID

        self.name = ""
        pass

    def get_ID(self):
        """returns __ID"""
        return self.__ID

    def get_as_element(self):
        """Gets object as elementtree object for printing to file."""
        import xml.etree.cElementTree as et
        a = et.Element("occupant", attrib={"id": str(self.get_ID()), "name": self.name})
        return a

    def __eq__(self, other):
        """Used for compareing ID between occupants"""
        if isinstance(other, Occupant):
            if other.get_ID() == self.get_ID():
                return True
        return False


class Person(Occupant):
    """The child of Occupant that is for persons traveling."""
    def __init__(self, ID, name):
        """Runs parrents constructor and sets name"""
        super().__init__(ID)
        self.name = name

    def __str__(self):
        return self.name

    def full_name(self):
        """For expandability. Returns name with capital first letters."""
        return self.name.capitalize()
