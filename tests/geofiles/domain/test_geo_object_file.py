from tests.geofiles.base_test import BaseTest


class TestGeoObjectFile(BaseTest):
    def test_get_vertex(self):
        # given
        cube = self.get_cube()

        # when
        vertex = cube.get_vertex(1)

        # then
        self.assertEqual(vertex, [14.2842865755919, 48.3028533074941, 279.307006835938])

    def test_get_vertex2(self):
        # given
        cube = self.get_cube()

        # when
        vertex = cube.get_vertex(-1)

        # then
        self.assertEqual(vertex, [14.2842730710157, 48.3028443243414, 279.307006835938])

    def test_get_vertex3(self):
        # given
        cube = self.get_cube()

        # when
        with self.assertRaises(Exception) as context:
            cube.get_vertex(0)

            # then
        self.assertTrue("Non valid index" in str(context.exception))

    def test_get_vertex4(self):
        # given
        cube = self.get_cube()

        # when
        with self.assertRaises(Exception) as context:
            cube.get_vertex("test")

            # then
        self.assertTrue("invalid literal for int()" in str(context.exception))

    def test_is_origin_based(self):
        # given
        cube = self.get_cube()

        # when
        origin_based = cube.is_origin_based()

        # then
        self.assertFalse(origin_based)

    def test_is_origin_based2(self):
        # given
        cube = self.get_cube(True)

        # when
        origin_based = cube.is_origin_based()

        # then
        self.assertTrue(origin_based)

    def test_is_geo_referenced(self):
        # given
        cube = self.get_cube(True)

        # when
        geo_referenced = cube.is_geo_referenced()

        # then
        self.assertTrue(geo_referenced)

    def test_is_geo_referenced2(self):
        # given
        cube = self.get_local_cube()

        # when
        geo_referenced = cube.is_geo_referenced()

        # then
        self.assertFalse(geo_referenced)
