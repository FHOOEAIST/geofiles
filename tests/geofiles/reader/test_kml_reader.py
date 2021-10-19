from geofiles.reader.kml_reader import KmlReader
from tests.geofiles.base_test import BaseTest


class TestKmlReader(BaseTest):
    def test_read(self) -> None:
        # given
        file = self.get_ressource_file("cube.kml")
        reader = KmlReader()
        reader.unique_vertices = True
        cube = self.get_cube()

        # when
        geo_obj_file = reader.read(file)

        # then
        self.assertTrue(geo_obj_file.is_geo_referenced())
        self.assertFalse(geo_obj_file.is_origin_based())
        self.assertEqual(len(geo_obj_file.objects), 1)
        self.assertEqual(len(geo_obj_file.objects[0].faces), 12)
        self.assertEqual(len(geo_obj_file.vertices), 8)
        self.assertEqual(geo_obj_file.crs, "urn:ogc:def:crs:OGC:2:84")

        for vertex in geo_obj_file.vertices:
            self.assertTrue(vertex in cube.vertices)

    def test_read2(self) -> None:
        # given
        file = self.get_ressource_file("cube.kml")
        reader = KmlReader()
        cube = self.get_cube()

        # when
        geo_obj_file = reader.read(file)

        # then
        self.assertTrue(geo_obj_file.is_geo_referenced())
        self.assertFalse(geo_obj_file.is_origin_based())
        self.assertEqual(len(geo_obj_file.objects), 1)
        self.assertEqual(len(geo_obj_file.objects[0].faces), 12)
        self.assertEqual(len(geo_obj_file.vertices), 36)
        self.assertEqual(geo_obj_file.crs, "urn:ogc:def:crs:OGC:2:84")

        for vertex in geo_obj_file.vertices:
            self.assertTrue(vertex in cube.vertices)
