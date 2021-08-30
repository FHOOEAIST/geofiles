class GeoObjectFile:
    """
    Basic class representing a file containing geo referenced object
    """

    def __init__(self):
        """
        Initializes a GeoObjectFile with the following attributes:
        - crs: name (string) of the used coordinate reference system
        - origin: geo-referenced origin (tuple) of the geo objects
        - translation: tuple containing the local translation of origin-based geo objects
        - rotation: tuple containing the local rotation of origin-based geo objects
        - scaling: tuple containing the local scaling of origin-based geo objects
        - objects: List of all geo-objects within this GeoObjectFile
        - vertices: List of all vertices within this GeoObjectFile
        - normals: List of all normals within this GeoObjectFile
        - texture_coordinates: List of all texture_coordinates within this GeoObjectFile
        """
        self.crs = None
        self.origin = None
        self.translation = None
        self.rotation = None
        self.scaling = None
        self.objects = []
        self.vertices = []
        self.normals = []
        self.texture_coordinates = []

    def is_origin_based(self) -> bool:
        """
        Checks if this GeoObjectFile is based on a geo referenced origin, or if all vertices are geo referenced
        :return: true iff file uses a origin
        """
        return self.origin is not None

    def is_geo_referenced(self) -> bool:
        """
        :return: true iff file is geo-referenced or a local file
        """
        return self.crs is not None

    def get_vertex(self, idx: int):
        """
        Returns the vertex at the given index (Note: indices are .obj style starting with 1 and tail indices < 0
        :param idx: idx to access
        :return: vertex at given index
        """
        return self._access_idx(self.vertices, idx)

    def get_normal(self, idx: int):
        """
        Returns the normal vertex at the given index (Note: indices are .obj style starting with 1 and tail indices < 0
        :param idx: idx to access
        :return: normal vertex at given index
        """
        return self._access_idx(self.normals, idx)

    def _access_idx(self, list_to_access, idx):
        """
        Access the given list using the given index (Note: indices are .obj style starting with 1 and tail indices < 0)
        :param list_to_access: list to be accessed
        :param idx: index
        :return: element in list at given index
        """
        idx = int(idx)

        if idx > 0:
            return list_to_access[idx - 1]
        elif idx < 0:
            return list_to_access[idx]
        else:
            raise Exception(f"Non valid index {idx}")
