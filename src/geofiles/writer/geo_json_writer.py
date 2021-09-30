from abc import ABC
from typing import Any, Dict, List

from geofiles.conversion.static import get_wgs_84
from geofiles.domain.geo_object_file import GeoObjectFile
from geofiles.writer.base import BaseWriter
from geofiles.writer.json_writer import JsonWriter


class GeoJsonWriter(JsonWriter, BaseWriter, ABC):
    """
    Writer implementation for creating GeoJSON geometry files
    """

    def create_json(
        self,
        data: GeoObjectFile,
        random_seed: Any = None,
    ) -> Dict[Any, Any]:
        if data.crs != get_wgs_84():
            raise Exception("GeoJSON (RFC 7946) requires WGS:84 coordinate system")

        if data.is_origin_based():
            raise Exception("Geo-referenced data must not be origin based")

        self._contains_transformation_information(data)

        res: Dict[Any, Any] = dict()
        res["type"] = "FeatureCollection"
        features: List[Any] = []
        res["features"] = features
        for obj in data.objects:
            if (
                obj.contains_scaling()
                or obj.contains_rotation()
                or obj.contains_translation()
            ):
                raise Exception(
                    "GeoJSON does not support local object transformation information"
                )
            polygon: Dict[Any, Any] = dict()
            polygon["type"] = "MultiPolygon"
            coordinates: List[Any] = []
            polygon["coordinates"] = coordinates
            for face in obj.faces:
                f = []
                for idx in face.indices:
                    vertex = data.get_vertex(idx)
                    f.append(vertex)
                f.append(data.get_vertex(face.indices[0]))
                coordinates.append([f])
            features.append(polygon)

        return res

    def get_file_type(self) -> str:
        """
        :return: the supported file type of this writer
        """
        return ".geo.json"
