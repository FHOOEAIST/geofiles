from abc import ABC
from typing import List, Any, Dict

from geofiles.domain.face import Face
from geofiles.domain.geo_object import GeoObject
from geofiles.domain.geo_object_file import GeoObjectFile
from geofiles.reader.base import BaseReader
from geofiles.reader.json_reader import JsonReader


class GeoJsonReader(JsonReader, BaseReader, ABC):
    """
    Reader implementation for GeoJSON files
    Note: That only certain FeatureCollection GeoJSONs with Polygons or MultiPolygons are supported
    """

    def __init__(self):
        """
        unique_vertices: defines that read vertices have to be unique
        """
        self.unique_vertices = False

    def _read_json(self, json_dict: Dict[Any, Any]) -> GeoObjectFile:
        if not json_dict.get("type") or json_dict.get("type") != "FeatureCollection":
            raise Exception("Only GeoJSONs with type FeatureCollection are supported")

        result = GeoObjectFile()
        result.crs = "urn:ogc:def:crs:OGC:2:84"
        vertex_list: List[List[Any]] = []
        vertex_indices: Dict[str, int] = dict()

        features = json_dict.get("features")
        for feature in features:
            if feature.get("type"):
                feature_type = feature.get("type")
                coordinates = feature.get("coordinates")

                faces = []
                if feature_type == "MultiPolygon":
                    for coordinate in coordinates:
                        inner_coordinates = []
                        self.get_values_of_most_inner_array(coordinate, inner_coordinates)
                        faces.append(inner_coordinates[:len(inner_coordinates) - 1])
                elif feature_type == "Polygon":
                    inner_coordinates = []
                    self.get_values_of_most_inner_array(coordinates, inner_coordinates)
                    faces.append(inner_coordinates[:len(inner_coordinates) - 1])

                geo_object = GeoObject()
                result.objects.append(geo_object)
                for face in faces:
                    face_object = Face()
                    geo_object.faces.append(face_object)
                    for idx, coordinate in enumerate(face):
                        self._filter_faces(self.unique_vertices, coordinate, face_object, vertex_list, vertex_indices)
        result.vertices = vertex_list
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
                res.append(input)
