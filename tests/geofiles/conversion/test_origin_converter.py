from geofiles.conversion.local_converter import OriginConverter
from tests.geofiles.base_test import BaseTest


class TestOriginConverter(BaseTest):
    def test_to_origin(self):
        # given
        converter = OriginConverter()
        cube = self.get_cube()

        # when
        origin_based = converter.to_origin(cube)

        # then
        self.assertAlmostEqual(origin_based.origin[0], 14.2842798233032)
        self.assertAlmostEqual(origin_based.origin[1], 48.30284881591775)
        self.assertAlmostEqual(origin_based.origin[2], 279.807006835938)

    def test_from_origin(self):
        # given
        converter = OriginConverter()
        cube = self.get_cube()
        cube.vertices = [
            [-0.5009357136907019, -0.4994462475020125, 0.5],
            [-0.5009357136907019, -0.4994462475020125, -0.5],
            [-0.5009356247086404, 0.4994462914230726, -0.5],
            [-0.5009356247086404, 0.4994462914230726, 0.5],
            [0.5009357136907018, -0.49944624750201255, -0.5],
            [0.5009356243927787, 0.4994462912395414, -0.5],
            [0.5009357136907018, -0.49944624750201255, 0.5],
            [0.5009356243927787, 0.4994462912395414, 0.5],
        ]
        cube.origin = [14.2842798233032, 48.30284881591775, 279.807006835938]
        res = self.get_cube()

        # when
        converted = converter.from_origin(cube)

        # then
        for idx, vertex in enumerate(converted.vertices):
            self.assertAlmostEqual(vertex[0], res.vertices[idx][0], 4)
            self.assertAlmostEqual(vertex[1], res.vertices[idx][1], 4)
            self.assertAlmostEqual(vertex[2], res.vertices[idx][2])
