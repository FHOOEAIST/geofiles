from geofiles.reader.geo_stl_reader import GeoStlReader
from tests.geofiles.base_test import BaseTest


class TestGeoStlReader(BaseTest):
    def test_read(self) -> None:
        # given
        file = self.get_ressource_file("cube.geostl")
        reader = GeoStlReader()

        # when
        geo_obj_file = reader.read(file)

        # then
        self.compare_with_cube(geo_obj_file)

    def test_read2(self) -> None:
        # given
        file = self.get_ressource_file("cube_origin.geostl")
        reader = GeoStlReader()

        # when
        geo_obj_file = reader.read(file)

        # then
        self.assertEqual(
            geo_obj_file.origin,
            [14.2842798233032, 48.30284881591775, 279.807006835938],
        )

    def test_read3(self) -> None:
        # given
        file = self.get_ressource_file("cube.stl")
        reader = GeoStlReader()

        # when
        geo_obj_file = reader.read(file)

        # then
        self.compare_geo_obj_files(geo_obj_file, self.get_local_cube())
