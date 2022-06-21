from typing import List, Optional, Dict, Any

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
        - meta_information: Meta information that additionally describe the object
        """
        self.name: str = ""
        self.parent: Optional[GeoObject] = None
        self.faces: List[Face] = []
        self.translation: Optional[List[float]] = None
        self.rotation: Optional[List[float]] = None
        self.scaling: Optional[List[float]] = None
        self.meta_information: Dict[str, Any] = dict()

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

    def get_type(self) -> Any:
        """
        Returns the type definition of the object
        """
        return self.get_meta_information_or_default("type", None)

    def set_type(self, val: str) -> None:
        """
        Setter for the type information
        :param val: value to be set
        """
        self.meta_information["type"] = val

    def get_meta_information_or_default(self, key: str, default: Any) -> Any:
        """
        Getter for meta information that returns the given default value if value is not available
        :param key: key of the meta information
        :param default: default value
        :returns: value for the given key or default
        """
        val = self.meta_information.get(key)
        if val is None:
            return default
        return val
