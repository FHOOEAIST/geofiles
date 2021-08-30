import unittest

from geofiles.conversion.origin_converter import OriginConverter
from geofiles.domain.face import Face
from geofiles.domain.geo_object import GeoObject
from geofiles.domain.geo_object_file import GeoObjectFile


class BaseTest(unittest.TestCase):
    def get_cube(self, origin_based: bool = False) -> GeoObjectFile:
        """
        :param origin_based: flag if cube should be origin based
        :return: A sample GeoObjectFile representing a geo-referenced cube
        """
        res = GeoObjectFile()
        res.crs = 'urn:ogc:def:crs:OGC:2:84'
        res.vertices = [
            [14.2842865755919, 48.3028533074941, 279.307006835938],
            [14.2842865755919, 48.3028533074941, 280.307006835938],
            [14.2842865755907, 48.3028443243414, 280.307006835938],
            [14.2842865755907, 48.3028443243414, 279.307006835938],
            [14.2842730710145, 48.3028533074941, 280.307006835938],
            [14.2842730710157, 48.3028443243414, 280.307006835938],
            [14.2842730710145, 48.3028533074941, 279.307006835938],
            [14.2842730710157, 48.3028443243414, 279.307006835938]
        ]
        geoobject = GeoObject()
        f1 = Face()
        f1.indices = [1, 2, 3]
        f2 = Face()
        f2.indices = [1, 3, 4]
        f3 = Face()
        f3.indices = [2, 5, 6]
        f4 = Face()
        f4.indices = [2, 6, 3]
        f5 = Face()
        f5.indices = [5, 7, 8]
        f6 = Face()
        f6.indices = [5, 8, 6]
        f7 = Face()
        f7.indices = [7, 1, 4]
        f8 = Face()
        f8.indices = [7, 4, 8]
        f9 = Face()
        f9.indices = [4, 3, 6]
        f10 = Face()
        f10.indices = [4, 6, 8]
        f11 = Face()
        f11.indices = [7, 5, 2]
        f12 = Face()
        f12.indices = [7, 2, 1]

        faces = [f1, f2, f3, f4, f5, f6, f7, f8, f9, f10, f11, f12]

        geoobject.faces = faces

        res.objects = [
            geoobject
        ]

        if origin_based:
            converter = OriginConverter()
            return converter.to_origin(res)

        return res

    def get_local_cube(self):
        """
        :return: A local geometry example of a cube without a referenced coordinate system
        """
        res = self.get_cube()
        res.crs = None
        res.vertices = [
            [-0.5, -0.5, 0.5],
            [-0.5, -0.5, -0.5],
            [-0.5, 0.5, -0.5],
            [-0.5, 0.5, 0.5],
            [0.5, -0.5, -0.5],
            [0.5, 0.5, -0.5],
            [0.5, -0.5, 0.5],
            [0.5, 0.5, 0.5]
        ]

        return res
