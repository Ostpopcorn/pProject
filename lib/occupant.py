class Occupant(object):
    def __init__(self,ID):
        self.__ID = ID
        pass

    def get_ID(self):
        return self.__ID

class Person(Occupant):
    def __init__(self, ID, name):
        super().__init__(ID)
        self.name = name

    def __str__(self):
        return  self.name

    def full_name(self):

        return self.name.capitalize()
