from geofiles.reader.geo_stl_reader import GeoStlReader
from tests.geofiles.base_test import BaseTest


class TestGeoStlReader(BaseTest):
    def test_read(self):
        # given
        file = self.get_ressource_file("cube.geostl")
        reader = GeoStlReader()

        # when
        geo_obj_file = reader.read(file)

        # then
        self.compare_with_cube(geo_obj_file)
