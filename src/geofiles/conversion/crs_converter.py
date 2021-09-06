import copy
from typing import Any, List

import pyproj

from geofiles.conversion.static import get_epsg_4326, get_wgs_84, update_min_max
from geofiles.domain.geo_object_file import GeoObjectFile


class CrsConverter:
    """
    Converter for projecting a given geo referenced object to another coordinate system
    """

    def convert(
        self,
        data: GeoObjectFile,
        target_crs: str,
        alwaysxy: bool = True,
        update_extent: bool = False,
    ) -> GeoObjectFile:
        """
        Converts the given data to another coordinate reference system
        :param data: to be converted
        :param target_crs: target coordinate system (string to create a pyproj.crs.CRS)
        :param alwaysxy: If true, the transform method will accept as input and return as output
            coordinates using the traditional GIS order, that is longitude, latitude
            for geographic CRS and easting, northing for most projected CRS.
            Default is false.
        :param update_extent: If true, extent information of the converted data is determined
        :return:
        """
        if data.crs is None:
            raise Exception("Given file is not geo-referenced")

        res = copy.deepcopy(data)
        res.crs = target_crs
        source = data.crs
        from_wgs84 = False
        if source == get_wgs_84():
            source = get_epsg_4326()
            from_wgs84 = True

        target = target_crs
        to_wgs84 = False
        if target_crs == get_wgs_84():
            target = get_epsg_4326()
            to_wgs84 = True
        transformer = pyproj.Transformer.from_crs(source, target, always_xy=alwaysxy)

        if data.is_origin_based() and data.origin is not None:
            res.origin = self._convert_coordinate(
                data.origin, transformer, from_wgs84, to_wgs84
            )

            if update_extent:
                res.update_extent()
        else:
            converted = []
            min_extent: List[float] = []
            max_extent: List[float] = []
            is_first = True
            for vertex in data.vertices:
                converted_vertex = self._convert_coordinate(
                    vertex, transformer, from_wgs84, to_wgs84
                )
                if is_first:
                    min_extent = list(converted_vertex).copy()
                    max_extent = list(converted_vertex).copy()
                    is_first = False
                else:
                    update_min_max(vertex, min_extent, max_extent)
                converted.append(converted_vertex)
            res.vertices = converted
        return res

    @staticmethod
    def _convert_coordinate(
        vertex: List[float], transformer: Any, from_wgs84: bool, to_wgs84: bool
    ) -> List[float]:
        """
        Converts the given vertex based on the given transformer with reference if input or output system is WGS84
        :param vertex: to be converted
        :param transformer: used to transform
        :param from_wgs84: is input wgs84 based?
        :param to_wgs84: is output wgs84 based?
        :return: converted coordinate
        """
        # if source is wgs we have to swap x and y to match EPSG:4326
        if not from_wgs84:
            x = vertex[0]
            y = vertex[1]
        else:
            x = vertex[1]
            y = vertex[0]

        transformed: List[float]
        if len(vertex) > 2:
            z = vertex[2]
            transformed = transformer.transform(x, y, z)
        else:
            transformed = transformer.transform(x, y)

        # if target is wgs we have to swap x and y to convert from EPSG:4326
        if to_wgs84:
            x = transformed[0]
            y = transformed[1]
            z = transformed[2]
            transformed = [y, x, z]
        return transformed
