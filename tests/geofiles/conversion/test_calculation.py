import unittest

from geofiles.conversion.calculation import *


class TestCalculation(unittest.TestCase):
    def test_get_distant_point(self) -> None:
        # given
        x = 0
        y = 0
        d = 1
        theta = 90

        # when
        res = get_distant_point(x, y, d, theta)

        # then
        self.assertAlmostEqual(res[0], 1.0)
        self.assertAlmostEqual(res[1], 0.0)

    def test_get_distant_point2(self) -> None:
        # given
        x = 0
        y = 0
        d = 1
        theta = 0

        # when
        res = get_distant_point(x, y, d, theta)

        # then
        self.assertAlmostEqual(res[0], 0.0)
        self.assertAlmostEqual(res[1], 1.0)

    def test_get_point_distance(self) -> None:
        # given
        p1 = [0, 0]
        p2 = [1, 0]

        # when
        d = get_point_distance(p1, p2)

        # then
        self.assertAlmostEqual(d, 1.0)

    def test_get_point_distance2(self) -> None:
        # given
        p1 = [0, 0]

        # when
        d = get_point_distance(p1, p1)

        # then
        self.assertAlmostEqual(d, 0.0)

    def test_get_angle_between_points(self) -> None:
        # given
        p1 = [0, 0]
        p2 = [0, 1]  # top

        # when
        theta = get_angle_between_points(p1, p2)

        # then
        self.assertAlmostEqual(theta, 0)

    def test_get_angle_between_points2(self) -> None:
        # given
        p1 = [0, 0]
        p2 = [1, 0]  # right

        # when
        theta = get_angle_between_points(p1, p2)

        # then
        self.assertAlmostEqual(theta, 90)

    def test_get_angle_between_points3(self) -> None:
        # given
        p1 = [0, 0]
        p2 = [0, -1]

        # when
        theta = get_angle_between_points(p1, p2)

        # then
        self.assertAlmostEqual(theta, 180)

    def test_get_angle_between_points4(self) -> None:
        # given
        p1 = [0, 0]
        p2 = [-1, 0]

        # when
        theta = get_angle_between_points(p1, p2)

        # then
        self.assertAlmostEqual(theta, 270)

    def test_get_center(self) -> None:
        # given
        vertices = [[-1, 0], [0, 1], [1, 0], [0, -1]]

        # when
        center = get_center(vertices)

        # then
        self.assertAlmostEqual(center[0], 0)
        self.assertAlmostEqual(center[1], 0)

    def test_get_center2(self) -> None:
        # given
        vertices = [[-1, 0, 2], [0, 1, 4], [1, 0, 2], [0, -1, 4]]

        # when
        center = get_center(vertices)

        # then
        self.assertAlmostEqual(center[0], 0)
        self.assertAlmostEqual(center[1], 0)
        self.assertAlmostEqual(center[2], 3)

    def test_rotate_point(self) -> None:
        # given
        point = [6, 0, 0]
        origin = [0, 0, 0]

        # when
        rotated_point = rotate_point(point, origin, 0, 0, 90)

        # then
        self.assertAlmostEqual(rotated_point[0], 0)
        self.assertAlmostEqual(rotated_point[1], 6)
        self.assertAlmostEqual(rotated_point[2], 0)

    def test_convert_obj_index(self) -> None:
        # given
        idx = 1
        list = [5, 3, 2]

        # when
        converted = convert_obj_index(idx, list)

        # then
        self.assertEqual(converted, 0)

    def test_convert_obj_index2(self) -> None:
        # given
        idx = -1
        list = [5, 3, 2]

        # when
        converted = convert_obj_index(idx, list)

        # then
        self.assertEqual(converted, 2)

    def test_convert_obj_index3(self) -> None:
        # given
        idx = 0
        list = [5, 3, 2]

        # when
        with self.assertRaises(Exception) as context:
            converted = convert_obj_index(idx, list)

        # then
        self.assertTrue("Index 0 not supported in OBJ" in str(context.exception))
