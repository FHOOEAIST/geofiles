import json
from abc import ABC
from typing import Iterable, List, Any, Dict

from geofiles.domain.face import Face
from geofiles.domain.geo_object import GeoObject
from geofiles.domain.geo_object_file import GeoObjectFile
from geofiles.reader.base import BaseReader
from geofiles.reader.json_reader import JsonReader


class CityJsonReader(JsonReader, BaseReader, ABC):
    """
    Reader implementation for CityJSON files
    Note: That there will be semantic loss if reading a CityJSON file (object classes, etc.)
    """

    def _read_json(self, json_dict: Dict[Any, Any]) -> GeoObjectFile:
       result = GeoObjectFile()

       if not json_dict.get("metadata"):
           raise Exception("No metadata defined (at least reference system is required)")

       metadata = json_dict["metadata"]

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
                result.objects.append(geo_object)
                geo_object.name = city_object_name
                geometry = city_object.get("geometry")
                if geometry:
                    for geometry_object in geometry:
                        boundaries = geometry_object.get("boundaries")
                        if boundaries:
                            faces = []
                            self.get_values_of_most_inner_array(boundaries, faces)
                            geo_object.faces = faces
       else:
           raise Exception("No city objects defined")

       return result

    def get_values_of_most_inner_array(self, input: List[Any], res: List[Any]) -> None:
        """
        iterates the given list and fills the res list with the most inner values
        """
        if len(input) > 0:
            elem = input[0]
            if isinstance(elem, list):
                for element in input:
                    self.get_values_of_most_inner_array(element, res)
            else:
                face = Face()
                for e in input:
                    face.indices.append(e + 1)
                res.append(face)