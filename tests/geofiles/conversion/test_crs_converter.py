from geofiles.conversion.crs_converter import *
from tests.geofiles.base_test import BaseTest


class TestCrsConverter(BaseTest):
    def test_convert(self):
        # given
        cube = self.get_cube()
        converter = CrsConverter()

        # when
        converted = converter.convert(cube, "urn:ogc:def:crs:EPSG::4326")

        # then
        for idx, vertex in enumerate(converted.vertices):
            ref = cube.vertices[idx]
            self.assertAlmostEqual(vertex[0], ref[1])
            self.assertAlmostEqual(vertex[1], ref[0])
            self.assertAlmostEqual(vertex[2], ref[2])

    def test_convert2(self):
        # given
        cube = self.get_cube()
        converter = CrsConverter()

        # when
        converted = converter.convert(cube, "EPSG:26915")

        # then
        self.assertAlmostEqual(converted.vertices[0][0], 4981328.249156999)
        self.assertAlmostEqual(converted.vertices[0][1], 17994606.922839668)
        self.assertAlmostEqual(converted.vertices[0][2], 279.307006835938)
