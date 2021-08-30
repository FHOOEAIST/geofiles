import copy

from geofiles.conversion.origin_converter import OriginConverter
from geofiles.domain.geo_object_file import GeoObjectFile


class LocalConverter:
    """
    Converter used to convert a geo referenced file to a local file or vice versa
    """

    def from_local(
        self, data: GeoObjectFile, crs: str, origin: list, origin_based: bool = True
    ):
        """
        Converts the given object file with a local coordinate system to a geo-referenced representation
        :param data: to be converted
        :param crs: target crs
        :param origin: origin point used for conversion
        :param origin_based: flag that signals if the final file should be origin based or should use geo-referenced vertices
        :return: geo-referenced file based on the given origin
        """
        if data.crs is not None:
            raise Exception("Given data is already geo-referenced")
        res = copy.deepcopy(data)
        res.crs = crs
        res.origin = origin
        if not origin_based:
            converter = OriginConverter()
            res = converter.from_origin(res)
        return res

    def to_local(self, data: GeoObjectFile):
        """
        Converts the given geo-referenced file to a local representation
        :param data: to be converted
        :return:
        """
        if not data.is_geo_referenced():
            raise Exception("Given data is already in local coordinates")

        if not data.is_origin_based():
            converter = OriginConverter()
            res = converter.to_origin(data)
        else:
            res = copy.deepcopy(data)

        res.origin = None
        res.crs = None

        return res
