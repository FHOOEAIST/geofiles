from geofiles.conversion.extent_calculation import ExtentCalculator
from tests.geofiles.base_test import BaseTest


class TestExtentCalculator(BaseTest):
    def test_update_extent(self) -> None:
        """
        Test update extent with: Global Coordinates
        """
        # given
        cube = self.get_cube()
        calculator = ExtentCalculator()

        # when
        updated = calculator.update_extent(cube)

        # then
        self.assertEqual(updated.max_extent, [14.2842865755919, 48.3028533074941, 280.307006835938])
        self.assertEqual(updated.min_extent, [14.2842730710145, 48.3028443243414, 279.307006835938])

    def test_update_extent2(self) -> None:
        """
        Test update extent with: Local Coordinates + Global Origin + Local Extent
        """
        # given
        cube = self.get_local_cube()
        calculator = ExtentCalculator()

        # when
        updated = calculator.update_extent(cube)

        # then
        self.assertEqual(updated.max_extent, [0.5, 0.5, 0.5])
        self.assertEqual(updated.min_extent, [-0.5, -0.5, -0.5])

    def test_update_extent3(self) -> None:
        """
        Test update extent with: Local Coordinates + Global Origin + Global Extent
        """
        # given
        cube = self.get_local_cube()
        cube.crs = "urn:ogc:def:crs:OGC:2:84"
        cube.origin = [14.2842798233032, 48.30284881591775, 279.807006835938]
        calculator = ExtentCalculator()

        # when
        updated = calculator.update_extent(cube, geospatial_extent=True)

        # then
        self.assertEqual(updated.max_extent, [14.284288077687554, 48.302856204513326, 280.307006835938])
        self.assertEqual(updated.min_extent, [14.284271568918845, 48.302854323051484, 279.307006835938])

    def test_update_extent4(self) -> None:
        """
        Test update extent with: Transformation + Local Extent
        """
        # given
        cube = self.get_local_cube()
        cube.crs = "urn:ogc:def:crs:OGC:2:84"
        cube.origin = [14.2842798233032, 48.30284881591775, 279.807006835938]

        cube.scaling = [2, 2, 2]
        calculator = ExtentCalculator()

        # when
        updated = calculator.update_extent(cube, include_transformation=True)

        # then
        self.assertEqual(updated.max_extent, [1, 1, 1])
        self.assertEqual(updated.min_extent, [-1, -1, -1])

    def test_update_extent5(self) -> None:
        """
        Test update extent with: Transformation + Global Extent
        """
        # given
        cube = self.get_cube()
        cube.translation = [10, 10, 10]
        calculator = ExtentCalculator()

        # when
        updated = calculator.update_extent(cube, geospatial_extent=True, include_transformation=True)

        # then
        self.assertEqual(updated.max_extent, [14.28411731249151, 48.30275232771007, 270.307006835938])
        self.assertEqual(updated.min_extent, [14.284095127597515, 48.30273672014227, 269.307006835938])

