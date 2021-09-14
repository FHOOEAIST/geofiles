from geofiles.reader.geo_off_reader import GeoOffReader
from tests.geofiles.base_test import BaseTest


class TestGeoOffReader(BaseTest):
    def test_read(self) -> None:
        # given
        file = self.get_ressource_file("cube.geooff")
        reader = GeoOffReader()

        # when
        geo_obj_file = reader.read(file)

        # then
        self.compare_with_cube(geo_obj_file)

    def test_read2(self) -> None:
        # given
        file = self.get_ressource_file("cube_origin.geooff")
        reader = GeoOffReader()

        # when
        geo_obj_file = reader.read(file)

        # then
        self.assertEqual(
            geo_obj_file.origin,
            [14.2842798233032, 48.30284881591775, 279.807006835938],
        )

    def test_read3(self) -> None:
        # given
        file = self.get_ressource_file("cube.off")
        reader = GeoOffReader()

        # when
        geo_obj_file = reader.read(file)

        # then
        self.compare_geo_obj_files(geo_obj_file, self.get_local_cube())

    def test_read4(self) -> None:
        # given
        file = self.get_ressource_file("cube_transformed.geooff")
        reader = GeoOffReader()

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

    def test_read5(self) -> None:
        # given
        file = self.get_ressource_file("cube_origin_extent.geooff")
        reader = GeoOffReader()

        # when
        geo_obj_file = reader.read(file)

        # then
        self.assertEqual(
            geo_obj_file.min_extent, [-0.5009357136907019, -0.49944624750201255, -0.5]
        )
        self.assertEqual(
            geo_obj_file.max_extent, [0.5009357136907018, 0.4994462914230726, 0.5]
        )
