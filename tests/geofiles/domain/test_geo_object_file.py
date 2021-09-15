from geofiles.domain.geo_object import GeoObject
from tests.geofiles.base_test import BaseTest


class TestGeoObjectFile(BaseTest):
    def test_get_vertex(self) -> None:
        # given
        cube = self.get_cube()

        # when
        vertex = cube.get_vertex(1)

        # then
        self.assertEqual(vertex, [14.2842865755919, 48.3028533074941, 279.307006835938])

    def test_get_vertex2(self) -> None:
        # given
        cube = self.get_cube()

        # when
        vertex = cube.get_vertex(-1)

        # then
        self.assertEqual(vertex, [14.2842730710157, 48.3028443243414, 279.307006835938])

    def test_get_vertex3(self) -> None:
        # given
        cube = self.get_cube()

        # when
        with self.assertRaises(Exception) as context:
            cube.get_vertex(0)

            # then
        self.assertTrue("Non valid index" in str(context.exception))

    def test_get_vertex4(self) -> None:
        # given
        cube = self.get_cube()

        # when
        with self.assertRaises(Exception) as context:
            cube.get_vertex("test")

            # then
        self.assertTrue("invalid literal for int()" in str(context.exception))

    def test_is_origin_based(self) -> None:
        # given
        cube = self.get_cube()

        # when
        origin_based = cube.is_origin_based()

        # then
        self.assertFalse(origin_based)

    def test_is_origin_based2(self) -> None:
        # given
        cube = self.get_cube(True)

        # when
        origin_based = cube.is_origin_based()

        # then
        self.assertTrue(origin_based)

    def test_is_geo_referenced(self) -> None:
        # given
        cube = self.get_cube(True)

        # when
        geo_referenced = cube.is_geo_referenced()

        # then
        self.assertTrue(geo_referenced)

    def test_is_geo_referenced2(self) -> None:
        # given
        cube = self.get_local_cube()

        # when
        geo_referenced = cube.is_geo_referenced()

        # then
        self.assertFalse(geo_referenced)

    def test_update_extent(self) -> None:
        # given
        cube = self.get_local_cube()

        # when
        cube.update_extent()

        # then
        self.assertEqual(cube.max_extent, [0.5, 0.5, 0.5])
        self.assertEqual(cube.min_extent, [-0.5, -0.5, -0.5])

    def test_contains_extent(self) -> None:
        # given
        cube = self.get_local_cube()

        # when
        cube.update_extent()

        # then
        self.assertTrue(cube.contains_extent())

    def test_contains_extent2(self) -> None:
        # given

        # when
        cube = self.get_local_cube()

        # then
        self.assertFalse(cube.contains_extent())

    def test_minimize(self) -> None:
        # given
        cube = self.get_local_cube()
        cube.objects.append(GeoObject())

        # when
        cube.minimize()

        # then
        self.assertEqual(len(cube.objects), 1)

    def test_minimize_2(self) -> None:
        # given
        cube = self.get_local_cube()
        cube.objects += cube.objects
        name = "test"

        # when
        cube.minimize(name)

        # then
        self.assertEqual(len(cube.objects), 1)
        self.assertEqual(cube.objects[0].name, name)
        self.assertEqual(len(cube.objects[0].faces), 12)

    def test_minimize_3(self) -> None:
        # given
        cube = self.get_local_cube()
        cube.objects += cube.objects
        cube.objects[0].scaling = [5, 5, 5]

        # when
        with self.assertRaises(Exception) as context:
            cube.minimize()

        # then
        self.assertTrue(
            "Can not minimize GeoObjectFile containing objects with local transformation."
            in str(context.exception)
        )
