import copy
from typing import Any, List

from geofiles.conversion.origin_converter import OriginConverter
from geofiles.domain.geo_object_file import GeoObjectFile


class LocalConverter:
    """
    Converter used to convert a geo referenced file to a local file or vice versa
    """

    @staticmethod
    def from_local(
        data: GeoObjectFile,
        crs: str,
        origin: List[Any],
        origin_based: bool = True,
        update_extent: bool = False,
    ) -> GeoObjectFile:
        """
        Converts the given object file with a local coordinate system to a geo-referenced representation
        :param data: to be converted
        :param crs: target crs
        :param origin: origin point used for conversion
        :param origin_based: flag that signals if the final file should be origin based or should use geo-referenced vertices
        :param update_extent: If true, extent information of the converted data is determined
        :return: geo-referenced file based on the given origin
        """
        if data.crs is not None:
            raise Exception("Given data is already geo-referenced")
        res = copy.deepcopy(data)
        res.crs = crs
        res.origin = origin
        if not origin_based:
            converter = OriginConverter()
            res = converter.from_origin(res, update_extent=update_extent)
        elif update_extent:
            res.update_extent()

        return res

    @staticmethod
    def to_local(data: GeoObjectFile, update_extent: bool = False) -> GeoObjectFile:
        """
        Converts the given geo-referenced file to a local representation
        :param data: to be converted
        :param update_extent: If true, extent information of the converted data is determined
        :return:
        """
        if not data.is_geo_referenced():
            raise Exception("Given data is already in local coordinates")

        res: GeoObjectFile
        if not data.is_origin_based():
            converter = OriginConverter()
            res = converter.to_origin(data, update_extent=update_extent)
        else:
            res = copy.deepcopy(data)
            if update_extent:
                res.update_extent()

        res.origin = None
        res.crs = None

        return res
