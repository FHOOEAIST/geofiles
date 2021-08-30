from geofiles.reader.geo_off_reader import GeoOffReader
from tests.geofiles.base_test import BaseTest


class TestGeoOffReader(BaseTest):
    def test_read(self):
        # given
        file = self.get_ressource_file("cube.geooff")
        reader = GeoOffReader()

        # when
        geo_obj_file = reader.read(file)

        # then
        self.compare_with_cube(geo_obj_file)

    def test_read2(self):
        # given
        file = self.get_ressource_file("cube_origin.geooff")
        reader = GeoOffReader()

        # when
        geo_obj_file = reader.read(file)

        # then
        self.assertEqual(geo_obj_file.origin, ['14.2842798233032', '48.30284881591775', '279.807006835938'])
