from typing import List, Optional

from geofiles.conversion.static import update_min_max
from geofiles.domain.geo_object import GeoObject


class GeoObjectFile:
    """
    Basic class representing a file containing geo referenced object
    """

    def __init__(self) -> None:
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
        - min_extent: minimal geographical extent of the vertices
        - max_extent: maximal geographical extent of the vertices
        """
        self.crs: Optional[str] = None
        self.origin: Optional[List[float]] = None
        self.translation: Optional[List[float]] = None
        self.rotation: Optional[List[float]] = None
        self.scaling: Optional[List[float]] = None
        self.objects: List[GeoObject] = []
        self.vertices: List[List[float]] = []
        self.normals: List[List[float]] = []
        self.texture_coordinates: List[List[float]] = []
        self.min_extent: Optional[List[float]] = []
        self.max_extent: Optional[List[float]] = []

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

    def get_vertex(self, idx: int) -> List[float]:
        """
        Returns the vertex at the given index (Note: indices are .obj style starting with 1 and tail indices < 0
        :param idx: idx to access
        :return: vertex at given index
        """
        return self._access_idx(self.vertices, idx)

    def get_normal(self, idx: int) -> List[float]:
        """
        Returns the normal vertex at the given index (Note: indices are .obj style starting with 1 and tail indices < 0
        :param idx: idx to access
        :return: normal vertex at given index
        """
        return self._access_idx(self.normals, idx)

    @staticmethod
    def _access_idx(list_to_access: List[List[float]], idx: int) -> List[float]:
        """
        Access the given list using the given index (Note: indices are .obj style starting with 1 and tail indices < 0)
        :param list_to_access: list to be accessed
        :param idx: index
        :return: element in list at given index
        """
        idx = int(idx)

        if idx > 0:
            return list_to_access[idx - 1]

        if idx < 0:
            return list_to_access[idx]

        raise Exception(f"Non valid index {idx}")

    def contains_extent(self) -> bool:
        """
        Checks if this geo-referenced fle contains extent information
        """
        return (
            self.min_extent is not None
            and self.max_extent is not None
            and len(self.min_extent) > 0
            and len(self.max_extent) > 0
        )

    def update_extent(self) -> None:
        """
        Updates the min and max extent values of this geo-referenced object file
        """
        if len(self.vertices) > 0:
            min_extent = self.vertices[0].copy()
            max_extent = self.vertices[0].copy()

            for vertex in self.vertices:
                update_min_max(vertex, min_extent, max_extent)

            self.min_extent = min_extent
            self.max_extent = max_extent
