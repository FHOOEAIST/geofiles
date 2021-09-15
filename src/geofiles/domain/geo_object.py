from typing import List, Optional

from geofiles.conversion.static import is_not_none_nor_empty
from geofiles.domain.face import Face


class GeoObject:
    """
    Class that represents a geo-referenced object
    """

    def __init__(self) -> None:
        """
        A geo-referenced object with the following attributes:
        - name: the name of the individual object
        - parent: reference to a parent object to represent a hierarchy
        - faces: a list of face-objects representing the geometry of this object
        - translation: tuple containing the local translation of origin-based geo objects
        - rotation: tuple containing the local rotation of origin-based geo objects
        - scaling: tuple containing the local scaling of origin-based geo objects
        """
        self.name: str = ""
        self.parent: Optional[GeoObject] = None
        self.faces: List[Face] = []
        self.translation: Optional[List[float]] = None
        self.rotation: Optional[List[float]] = None
        self.scaling: Optional[List[float]] = None

    def contains_scaling(self) -> bool:
        """
        Checks if this geo-referenced file contains global scaling information
        """
        return is_not_none_nor_empty(self.scaling) and self.scaling != [1.0, 1.0, 1.0]

    def contains_translation(self) -> bool:
        """
        Checks if this geo-referenced file contains global translation information
        """
        return is_not_none_nor_empty(self.translation) and self.translation != [
            0.0,
            0.0,
            0.0,
        ]

    def contains_rotation(self) -> bool:
        """
        Checks if this geo-referenced file contains global rotation information
        """
        return is_not_none_nor_empty(self.rotation) and self.rotation != [0.0, 0.0, 0.0]
