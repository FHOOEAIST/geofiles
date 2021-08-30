from geofiles.conversion.local_converter import LocalConverter
from tests.geofiles.base_test import BaseTest


class TestLocalConverter(BaseTest):
    def test_from_local(self):
        # given
        cube = self.get_local_cube()
        converter = LocalConverter()
        crs = 'urn:ogc:def:crs:OGC:2:84'
        origin = [14.2842798233032, 48.30284881591775, 279.807006835938]

        # when
        converted = converter.from_local(cube, crs, origin)

        # then
        self.assertEqual(converted.crs, crs)
        self.assertEqual(converted.origin, origin)

    def test_from_local2(self):
        # given
        cube = self.get_local_cube()
        converter = LocalConverter()
        crs = 'urn:ogc:def:crs:OGC:2:84'
        origin = [14.2842798233032, 48.30284881591775, 279.807006835938]
        res = [[14.284283514776243, 48.302856204513326, 280.307006835938], [14.284283514776243, 48.302856204513326, 279.307006835938], [14.284288077687554, 48.302854323051484, 279.307006835938], [14.284288077687554, 48.302854323051484, 280.307006835938], [14.284276131830156, 48.302856204513326, 279.307006835938], [14.284271568918845, 48.302854323051484, 279.307006835938], [14.284276131830156, 48.302856204513326, 280.307006835938], [14.284271568918845, 48.302854323051484, 280.307006835938]]

        # when
        converted = converter.from_local(cube, crs, origin, False)

        # then
        for idx, vertex in enumerate(converted.vertices):
            self.assertAlmostEqual(vertex[0], res[idx][0])
            self.assertAlmostEqual(vertex[1], res[idx][1])
            self.assertAlmostEqual(vertex[2], res[idx][2])

    def test_to_local(self):
        # given
        cube = self.get_cube()
        converter = LocalConverter()
        res = [[-0.5009357136907019, -0.4994462475020125, 0.5], [-0.5009357136907019, -0.4994462475020125, -0.5], [-0.5009356247086404, 0.4994462914230726, -0.5], [-0.5009356247086404, 0.4994462914230726, 0.5], [0.5009357136907018, -0.49944624750201255, -0.5], [0.5009356243927787, 0.4994462912395414, -0.5], [0.5009357136907018, -0.49944624750201255, 0.5], [0.5009356243927787, 0.4994462912395414, 0.5]]

        # when
        local = converter.to_local(cube)

        # then
        for idx, vertex in enumerate(local.vertices):
            self.assertAlmostEqual(vertex[0], res[idx][0])
            self.assertAlmostEqual(vertex[1], res[idx][1])
            self.assertAlmostEqual(vertex[2], res[idx][2])
