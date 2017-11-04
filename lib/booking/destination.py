class Destination(object):
    @classmethod
    def read_from_file(cls,et):
        b = et.find("Destination")
        a = Destination(et.attrib["name"])
        return a

    def __init__(self, place_name):
        self.name = place_name

    def get_as_element(self):
        import xml.etree.cElementTree as et
        a = et.Element("Destination", attrib={"name": self.name})
        return a
