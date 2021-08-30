from pyproj import Geod
from geofiles.conversion.calculation import *

from geofiles.domain.geo_object_file import GeoObjectFile
from geofiles.conversion.static import get_lon_lat, get_epsg_4326, get_wgs_84


class OriginConverter:
    """
    Converter used to convert a geo referenced file to a origin based representation or vice versa
    """

    def to_origin(self, data: GeoObjectFile, origin: list = None, bearing_offset: float = 0.0):
        """
        Converts the given file to an origin based representation
        :param data: to be converted
        :param origin: coordinate used as file origin
        :param bearing_offset: angle offset between the origin's coordinate system and the local vertices' coordinate system
        :return: origin based representation
        """
        if data.is_origin_based():
            raise Exception("Given geo-referenced object file is already origin based")

        if data.crs != get_wgs_84() and data.crs != get_epsg_4326():
            raise Exception(f"Function only supported for \"{get_wgs_84()}\" and \"{get_epsg_4326()}\"")

        res = copy.deepcopy(data)
        if origin is None:
            localorigin = get_center(data.vertices)
        else:
            localorigin = origin

        res.origin = localorigin

        new_vertices = []
        geod = Geod(ellps='WGS84')
        for vertex in data.vertices:
            lon0, lat0 = get_lon_lat(vertex, data.crs)
            lon1, lat1 = get_lon_lat(localorigin, data.crs)
            bearing, _, distance = geod.inv(lon0, lat0, lon1, lat1)
            new_vertex = get_distant_point(0, 0, distance, bearing + bearing_offset)
            new_vertex.append(localorigin[2] - vertex[2])
            new_vertices.append(new_vertex)

        res.vertices = new_vertices

        return res

    def from_origin(self, data: GeoObjectFile, bearing_offset: float = 0.0):
        """
        Converts the given file from an origin based representation
        :param data: to be converted
        :param bearing_offset: angle offset between the origin's coordinate system and the local vertices' coordinate system
        :return: non-origin based representation
        """
        if not data.is_origin_based():
            raise Exception("Given geo-referenced object file is not origin based")

        if data.crs != get_wgs_84() and data.crs != get_epsg_4326():
            raise Exception(f"Function only supported for \"{get_wgs_84()}\" and \"{get_epsg_4326()}\"")

        res = copy.deepcopy(data)
        res.origin = None
        origin_lon, origin_lat = get_lon_lat(data.origin, data.crs)

        new_vertices = []
        geod = Geod(ellps='WGS84')
        origin = [0, 0, 0]
        north_vector = [0, 1]
        for vertex in data.vertices:
            distance = get_point_distance(origin, vertex)
            r = get_angle_between_points(vertex, north_vector) + bearing_offset
            new_vertex = geod.fwd(origin_lon, origin_lat, r, distance)
            if data.crs == get_wgs_84():
                new_vertices.append([new_vertex[0], new_vertex[1], data.origin[2] - vertex[2]])
            else:
                new_vertices.append([new_vertex[1], new_vertex[0], data.origin[2] - vertex[2]])

        res.vertices = new_vertices
        return res
