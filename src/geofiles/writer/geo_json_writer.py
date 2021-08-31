import json
from abc import ABC
from io import TextIOWrapper

from geofiles.conversion.static import get_wgs_84
from geofiles.domain.geo_object import GeoObject
from geofiles.domain.geo_object_file import GeoObjectFile
from geofiles.writer.base import BaseWriter


class GeoJsonWriter(BaseWriter, ABC):
    """
    Writer implementation for creating GeoJSON geometry files
    """

    def _write(
        self, file: TextIOWrapper, data: GeoObjectFile, write_binary: bool, random_seed: any
    ) -> None:
        """
        Write implementation
        :param file: target to be written
        :param data: content to be written
        :param write_binary: flag if file is a binary file
        :return:
        """
        if data.crs != get_wgs_84():
            raise Exception("GeoJSON (RFC 7946) requires WGS:84 coordinate system")

        if data.is_origin_based():
            raise Exception("Geo-referenced data must not be origin based")

        self._contains_transformation_information(data)

        res = dict()
        res["type"] = "FeatureCollection"
        features = []
        res["features"] = features
        for obj in data.objects:
            obj: GeoObject = obj
            polygon = dict()
            polygon["type"] = "MultiPolygon"
            coordinates = []
            polygon["coordinates"] = coordinates
            for face in obj.faces:
                f = []
                for idx in face.indices:
                    vertex = data.get_vertex(idx)
                    f.append(vertex)
                f.append(data.get_vertex(face.indices[0]))
                coordinates.append([f])
            features.append(polygon)

        json.dump(res, file)

    def get_file_type(self) -> str:
        """
        :return: the supported file type of this writer
        """
        return ".geo.json"
