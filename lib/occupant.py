class Occupant(object):
    def __init__(self):
        pass


class Person(Occupant):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def full_name(self):

        return self.name.capitalize()
