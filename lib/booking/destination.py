class Destination(object):
    """Just keeps a name of the place."""
    @classmethod
    def read_from_file(cls,et):
        """reads from elementtree fromat"""
        b = et.find("Destination")
        a = Destination(et.attrib["name"])
        return a

    def __init__(self, place_name):
        """sets place_name"""
        self.name = place_name

    def get_as_element(self):
        """Gets a elementtree format for printing."""
        import xml.etree.cElementTree as et
        a = et.Element("Destination", attrib={"name": self.name})
        return a
