from geofiles.conversion.transformer import *
from tests.geofiles.base_test import BaseTest


class TestTransformer(BaseTest):
    def test_rotate(self) -> None:
        # given
        cube = self.get_cube(True)
        transformer = Transformer()
        cube.rotation = [45, 0, 0]
        res = [
            [-0.500935713690702, -0.7067152126214701, 0.0003915466504302856],
            [-0.500935713690702, 0.00039156856507752136, -0.7067152345361173],
            [-0.5009356247086405, 0.7067152565156527, -0.00039154658554213517],
            [-0.5009356247086405, -0.0003915246708948994, 0.7067152346010055],
            [0.5009357136907018, 0.00039156856507746585, -0.7067152345361174],
            [0.5009356243927787, 0.7067152563858764, -0.0003915467153183805],
            [0.5009357136907018, -0.7067152126214702, 0.00039154665043023007],
            [0.5009356243927787, -0.0003915248006711447, 0.7067152344712292],
        ]

        # when
        rotated = transformer.rotate(cube)

        # then
        for idx, vertex in enumerate(rotated.vertices):
            self.assertEqual(vertex, res[idx])

    def test_translate(self) -> None:
        # given
        cube = self.get_cube(True)
        transformer = Transformer()
        cube.translation = [5, -5, 10]

        # when
        translated = transformer.translate(cube)

        # then
        for idx, vertex in enumerate(translated.vertices):
            self.assertAlmostEqual(vertex[0], cube.vertices[idx][0] + 5)
            self.assertAlmostEqual(vertex[1], cube.vertices[idx][1] - 5)
            self.assertAlmostEqual(vertex[2], cube.vertices[idx][2] + 10)

    def test_scale(self) -> None:
        # given
        cube = self.get_cube(True)
        transformer = Transformer()
        cube.scaling = [2, 5, 7]

        # when
        scaled = transformer.scale(cube)

        # then
        for idx, vertex in enumerate(scaled.vertices):
            self.assertAlmostEqual(vertex[0], cube.vertices[idx][0] * 2, 5)
            self.assertAlmostEqual(vertex[1], cube.vertices[idx][1] * 5, 5)
            self.assertAlmostEqual(vertex[2], cube.vertices[idx][2] * 7, 5)

    def test_transform(self) -> None:
        # given
        cube = self.get_cube(True)
        transformer = Transformer()
        cube.rotation = [90, 0, 0]
        cube.translation = [5, 5, 5]
        cube.scaling = [2, 2, 2]

        res = [
            [3.9981285726975617, 4.000000021914647, 4.001107461166681],
            [3.9981285726975617, 6.000000021914647, 4.00110746116668],
            [3.9981287506616843, 6.000000021914647, 5.99889253901685],
            [3.9981287506616843, 4.000000021914647, 5.998892539016851],
            [6.001871427460369, 6.000000021914647, 4.00110746116668],
            [6.001871248864523, 6.000000021914647, 5.998892538649788],
            [6.001871427460369, 4.000000021914647, 4.00110746116668],
            [6.001871248864523, 4.000000021914647, 5.998892538649788],
        ]

        # when
        transformed = transformer.transform(cube)

        # then
        for idx, vertex in enumerate(transformed.vertices):
            self.assertEqual(vertex, res[idx])
