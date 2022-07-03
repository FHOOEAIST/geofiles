import copy
from typing import Any, Dict, List, Optional

from geofiles.conversion.static import is_not_none_nor_empty, update_min_max
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
        - translation: tuple containing the global translation of origin-based geo objects
        - rotation: tuple containing the global rotation of origin-based geo objects
        - scaling: tuple containing the global scaling of origin-based geo objects
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
        self.meta_information: Dict[str, Any] = dict()

    def get_translation_unit(self) -> str:
        """
        Getter for the translational unit
        :returns: unit used for translation information
        """
        tu = self.meta_information.get("tu")
        if tu is None:
            return "m"
        return str(tu)

    def get_rotation_unit(self) -> str:
        """
        Getter for the rotational unit
        :returns: unit used for rotation information
        """
        ru = self.meta_information.get("ru")
        if ru is None:
            return "deg"
        return str(ru)

    def is_default_translation_unit(self) -> bool:
        """
        :returns: true iff file uses metres as translation unit
        """
        return self.get_translation_unit() == "m"

    def is_default_rotation_unit(self) -> bool:
        """
        :returns: true iff file uses degree as rotation unit
        """
        return self.get_rotation_unit() == "deg"

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
        Checks if this geo-referenced file contains extent information
        """
        return is_not_none_nor_empty(self.min_extent) and is_not_none_nor_empty(
            self.max_extent
        )

    def contains_scaling(self) -> bool:
        """
        Checks if this geo-referenced file contains global scaling information
        """
        return is_not_none_nor_empty(self.scaling)

    def contains_translation(self) -> bool:
        """
        Checks if this geo-referenced file contains global translation information
        """
        return is_not_none_nor_empty(self.translation)

    def contains_rotation(self) -> bool:
        """
        Checks if this geo-referenced file contains global rotation information
        """
        return is_not_none_nor_empty(self.rotation)

    def update_extent(self) -> None:
        """
        Updates the min and max extent values of this geo-referenced object file, it does not consider if the file is origin based,
        nor any transformation information. For a more advanced functionality use the ExtentCalculator class
        """
        if len(self.vertices) > 0:
            min_extent = list(copy.deepcopy(self.vertices[0]))
            max_extent = list(copy.deepcopy(self.vertices[0]))

            for vertex in self.vertices:
                update_min_max(vertex, min_extent, max_extent)

            self.min_extent = min_extent
            self.max_extent = max_extent

    def minimize(self, name: Optional[str] = None) -> None:
        """
        Minimizes this GeoObjectFile to one single object as required for GeoOFF and GeoPLY. Also eliminates duplicated faces.
        Note: Object based meta information is lost, but file based information will be maintained.
        :param name: Name for the single object, if None the name of the first object is used
        """
        geoobject = GeoObject()

        use_first_elements_name = False
        if name is not None:
            geoobject.name = name
        else:
            use_first_elements_name = True

        face_set = set()
        for old_object in self.objects:
            if (
                old_object.contains_translation()
                or old_object.contains_scaling()
                or old_object.contains_rotation()
            ):
                raise Exception(
                    "Can not minimize GeoObjectFile containing objects with local transformation."
                )
            if use_first_elements_name:
                geoobject.name = old_object.name
                use_first_elements_name = False

            for face in old_object.faces:
                face_set.add(face)

        geoobject.faces = list(face_set)

        self.objects.clear()
        self.objects.append(geoobject)
