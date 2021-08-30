class GeoObject:
    """
    Class that represents a geo-referenced object
    """

    def __init__(self):
        """
        A geo-referenced object with the following attributes:
        - name: the name of the individual object
        - parent: reference to a parent object to represent a hierarchy
        - faces: a list of face-objects representing the geometry of this object
        """
        self.name = ""
        self.parent = None
        self.faces = []
