from geofiles.reader.geo_ply_reader import GeoPlyReader
from tests.geofiles.base_test import BaseTest


class TestGeoPlyReader(BaseTest):
    def test_read(self) -> None:
        # given
        file = self.get_ressource_file("cube.geoply")
        reader = GeoPlyReader()

        # when
        geo_obj_file = reader.read(file)

        # then
        self.compare_with_cube(geo_obj_file)

    def test_read2(self) -> None:
        # given
        file = self.get_ressource_file("cube_origin.geoply")
        reader = GeoPlyReader()

        # when
        geo_obj_file = reader.read(file)

        # then
        self.assertEqual(
            geo_obj_file.origin,
            [14.2842798233032, 48.30284881591775, 279.807006835938],
        )

    def test_read3(self) -> None:
        # given
        file = self.get_ressource_file("cube_transformed.geoply")
        reader = GeoPlyReader()

        # when
        geo_obj_file = reader.read(file)

        # then
        self.assertEqual(
            geo_obj_file.origin,
            [14.2842798233032, 48.30284881591775, 279.807006835938],
        )
        self.assertEqual(geo_obj_file.translation, [10, 50, 100])
        self.assertEqual(geo_obj_file.scaling, [2, 2, 2])
        self.assertEqual(geo_obj_file.rotation, [90, 0, 0])
