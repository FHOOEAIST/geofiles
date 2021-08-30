from geofiles.reader.geo_ply_reader import GeoPlyReader
from tests.geofiles.base_test import BaseTest


class TestGeoPlyReader(BaseTest):
    def test_read(self):
        # given
        file = self.get_ressource_file("cube.geoply")
        reader = GeoPlyReader()

        # when
        geo_obj_file = reader.read(file)

        # then
        self.compare_with_cube(geo_obj_file)
