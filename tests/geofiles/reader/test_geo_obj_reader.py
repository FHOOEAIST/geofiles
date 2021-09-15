from geofiles.reader.geo_obj_reader import GeoObjReader
from tests.geofiles.base_test import BaseTest


class TestGeoObjReader(BaseTest):
    def test_read(self) -> None:
        # given
        file = self.get_ressource_file("cube.geoobj")
        reader = GeoObjReader()
        cube = self.get_cube()

        # when
        geo_obj_file = reader.read(file)

        # then
        self.assertTrue(geo_obj_file.is_geo_referenced())
        self.assertFalse(geo_obj_file.is_origin_based())
        self.assertEqual(len(geo_obj_file.objects), 1)
        self.assertEqual(geo_obj_file.objects[0].name, "cube")
        self.assertEqual(len(geo_obj_file.objects[0].faces), 12)
        self.assertEqual(len(geo_obj_file.vertices), 8)
        self.assertEqual(geo_obj_file.crs, "urn:ogc:def:crs:OGC:2:84")

        for idx, face in enumerate(geo_obj_file.objects[0].faces):
            for inneridx, i in enumerate(face.indices):
                self.assertEqual(
                    int(i), int(cube.objects[0].faces[idx].indices[inneridx])
                )

        for idx, vertex in enumerate(geo_obj_file.vertices):
            self.assertAlmostEqual(float(vertex[0]), cube.vertices[idx][0])
            self.assertAlmostEqual(float(vertex[1]), cube.vertices[idx][1])
            self.assertAlmostEqual(float(vertex[2]), cube.vertices[idx][2])

    def test_read2(self) -> None:
        # given
        file = self.get_ressource_file("cube.obj")
        reader = GeoObjReader()
        cube = self.get_local_cube()

        # when
        geo_obj_file = reader.read(file)

        # then
        self.assertFalse(geo_obj_file.is_geo_referenced())
        self.assertFalse(geo_obj_file.is_origin_based())
        self.assertEqual(len(geo_obj_file.objects), 1)
        self.assertEqual(geo_obj_file.objects[0].name, "cube")
        self.assertEqual(len(geo_obj_file.objects[0].faces), 12)
        self.assertEqual(len(geo_obj_file.vertices), 8)

        for idx, face in enumerate(geo_obj_file.objects[0].faces):
            for inneridx, i in enumerate(face.indices):
                self.assertEqual(
                    int(i), int(cube.objects[0].faces[idx].indices[inneridx])
                )

        for idx, vertex in enumerate(geo_obj_file.vertices):
            self.assertAlmostEqual(float(vertex[0]), cube.vertices[idx][0])
            self.assertAlmostEqual(float(vertex[1]), cube.vertices[idx][1])
            self.assertAlmostEqual(float(vertex[2]), cube.vertices[idx][2])

    def test_read3(self) -> None:
        # given
        file = self.get_ressource_file("cube_origin.geoobj")
        reader = GeoObjReader()

        # when
        geo_obj_file = reader.read(file)

        # then
        self.assertEqual(
            geo_obj_file.origin,
            [14.2842798233032, 48.30284881591775, 279.807006835938],
        )

    def test_read4(self) -> None:
        # given
        file = self.get_ressource_file("cube_transformed.geoobj")
        reader = GeoObjReader()

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
        file = self.get_ressource_file("cube_origin_extent.geoobj")
        reader = GeoObjReader()

        # when
        geo_obj_file = reader.read(file)

        # then
        self.assertEqual(
            geo_obj_file.min_extent, [-0.5009357136907019, -0.49944624750201255, -0.5]
        )
        self.assertEqual(
            geo_obj_file.max_extent, [0.5009357136907018, 0.4994462914230726, 0.5]
        )

    def test_read6(self) -> None:
        # given
        file = self.get_ressource_file("cube_transformed_local.geoobj")
        reader = GeoObjReader()

        # when
        geo_obj_file = reader.read(file)

        # then
        self.assertEqual(
            geo_obj_file.origin,
            [14.2842798233032, 48.30284881591775, 279.807006835938],
        )
        self.assertEqual(geo_obj_file.objects[0].translation, [10, 50, 100])
        self.assertEqual(geo_obj_file.objects[0].scaling, [2, 2, 2])
        self.assertEqual(geo_obj_file.objects[0].rotation, [90, 0, 0])
