from abc import ABC
from typing import Any, Dict, List

from geofiles.domain.face import Face
from geofiles.domain.file_version import CityJsonVersion
from geofiles.domain.geo_object import GeoObject
from geofiles.domain.geo_object_file import GeoObjectFile
from geofiles.reader.base import BaseReader
from geofiles.reader.json_reader import JsonReader


class CityJsonReader(JsonReader, BaseReader, ABC):
    """
    Reader implementation for CityJSON files
    Note: That there will be semantic loss if reading a CityJSON file (object classes, etc.)
    """

    def __init__(
        self,
        version: CityJsonVersion = CityJsonVersion.V1_1,
        ignore_mandatory_transform: bool = False,
        use_transform_for_origin: bool = False
    ):
        """
        :param version: The CityJSON version to be used
        :param ignore_mandatory_transform: Starting with CityJSON v1.1 the Transform information is mandatory. Ignore this, when reading the file.
        :param use_transform_for_origin: If true, reader will use transform information as origin information
        """
        self.version = version
        self.ignore_mandatory_transform = ignore_mandatory_transform
        self.use_transform_for_origin = use_transform_for_origin

    def read_json(self, json_dict: Dict[Any, Any]) -> GeoObjectFile:
        result = GeoObjectFile()

        if not json_dict.get("metadata"):
            raise Exception(
                "No metadata defined (at least reference system is required)"
            )

        metadata = json_dict["metadata"]

        transform = json_dict.get("transform")
        if (
            self.version != CityJsonVersion.V1_0
            and transform is None
            and not self.ignore_mandatory_transform
        ):
            raise Exception("Transform information is mandatory in CityJSON >= 1.1")

        if transform is not None:
            translate = transform["translate"]
            if self.use_transform_for_origin:
                result.origin = translate
            else:
                result.translation = translate
            scale = transform["scale"]
            result.scaling = scale

        if metadata.get("referenceSystem"):
            result.crs = metadata.get("referenceSystem")
        else:
            raise Exception("Unknown reference system in input file.")

        if metadata.get("geographicalExtent"):
            extents = metadata["geographicalExtent"]
            result.min_extent = extents[:3]
            result.max_extent = extents[3:]

        if json_dict.get("vertices"):
            result.vertices = json_dict["vertices"]
        else:
            raise Exception("Undefined vertices in input file.")

        if json_dict.get("CityObjects"):
            city_objects = json_dict["CityObjects"]
            for city_object_name, city_object in city_objects.items():
                geo_object = GeoObject()
                geo_object.set_type(city_object["type"])
                result.objects.append(geo_object)
                geo_object.name = city_object_name
                geometry = city_object.get("geometry")
                if geometry:
                    for geometry_object in geometry:
                        boundaries = geometry_object.get("boundaries")
                        if boundaries:
                            faces: List[Face] = []
                            self.get_values_of_most_inner_array(boundaries, faces)
                            geo_object.faces = faces
        else:
            raise Exception("No city objects defined")

        return result

    def get_values_of_most_inner_array(
        self, input_list: List[Any], res: List[Any]
    ) -> None:
        """
        iterates the given list and fills the res list with the most inner values
        :param input_list: to be iterated
        :param res: Result list containing the most inner list elements
        """
        if len(input_list) > 0:
            elem = input_list[0]
            if isinstance(elem, list):
                for element in input_list:
                    self.get_values_of_most_inner_array(element, res)
            else:
                face = Face()
                for e in input_list:
                    face.indices.append(e + 1)
                res.append(face)

    def supports_origin_base(self) -> bool:
        """
        :return: true if writer supports origin based representation
        """
        return self.use_transform_for_origin
