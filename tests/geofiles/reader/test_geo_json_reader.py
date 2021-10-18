import json

from geofiles.reader.geo_json_reader import GeoJsonReader
from tests.geofiles.base_test import BaseTest


class TestGeoJsonReader(BaseTest):
    def test_read(self) -> None:
        # given
        file = self.get_ressource_file("cube.geo.json")
        reader = GeoJsonReader()
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

    def test_read2(self) -> None:
        # given
        file = self.get_ressource_file("cube.geo.json")
        reader = GeoJsonReader()
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

    def test_read3(self) -> None:
        # given
        file = self.get_ressource_file("cube.city.json")
        with open(file) as json_file:
            j = json.load(json_file)
            j["type"] = "test"
            reader = GeoJsonReader()
            cube = self.get_cube()

            # when
            with self.assertRaises(Exception) as context:
                geo_obj_file = reader.read_string(json.dumps(j))

            # then
            self.assertTrue("Only GeoJSONs with type FeatureCollection are supported" in str(context.exception))
