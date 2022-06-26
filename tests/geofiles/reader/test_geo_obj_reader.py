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

    def test_read7(self) -> None:
        # given
        file = self.get_ressource_file("cube_meta.geoobj")
        reader = GeoObjReader()

        # when
        geo_obj_file = reader.read(file)

        # then
        self.assertEqual(geo_obj_file.rotation_unit, "rad")
        self.assertEqual(geo_obj_file.translation_unit, "inch")
        self.assertEqual(
            geo_obj_file.objects[0].meta_information["type"], "GenericObject"
        )

    def test_read8(self) -> None:
        # given
        file = self.get_ressource_file("cube_meta2.geoobj")
        reader = GeoObjReader()

        # when
        geo_obj_file = reader.read(file)

        # then
        self.assertEqual(geo_obj_file.rotation_unit, "rad")
        self.assertEqual(geo_obj_file.translation_unit, "inch")
        self.assertEqual(
            geo_obj_file.objects[0].meta_information["axis_ordering"], ("x", "y", "z")
        )

    def test_read_string(self) -> None:
        # given
        input_str = """
            crs urn:ogc:def:crs:OGC:2:84
            v 14.2842865755919 48.3028533074941 279.307006835938
            v 14.2842865755919 48.3028533074941 280.307006835938
            v 14.2842865755907 48.3028443243414 280.307006835938
            v 14.2842865755907 48.3028443243414 279.307006835938
            v 14.2842730710145 48.3028533074941 280.307006835938
            v 14.2842730710157 48.3028443243414 280.307006835938
            v 14.2842730710145 48.3028533074941 279.307006835938
            v 14.2842730710157 48.3028443243414 279.307006835938
            o cube
            f 1 2 3
            f 1 3 4
            f 2 5 6
            f 2 6 3
            f 5 7 8
            f 5 8 6
            f 7 1 4
            f 7 4 8
            f 4 3 6
            f 4 6 8
            f 7 5 2
            f 7 2 1
            """
        reader = GeoObjReader()

        # when
        geo_obj_file = reader.read_string(input_str)

        # then
        self.assertTrue(geo_obj_file.is_geo_referenced())
        self.assertFalse(geo_obj_file.is_origin_based())
        self.assertEqual(len(geo_obj_file.objects), 1)
        self.assertEqual(geo_obj_file.objects[0].name, "cube")
        self.assertEqual(len(geo_obj_file.objects[0].faces), 12)
        self.assertEqual(len(geo_obj_file.vertices), 8)

    def test_read_strings(self) -> None:
        # given
        input_str = """
            crs urn:ogc:def:crs:OGC:2:84
            v 14.2842865755919 48.3028533074941 279.307006835938
            v 14.2842865755919 48.3028533074941 280.307006835938
            v 14.2842865755907 48.3028443243414 280.307006835938
            v 14.2842865755907 48.3028443243414 279.307006835938
            v 14.2842730710145 48.3028533074941 280.307006835938
            v 14.2842730710157 48.3028443243414 280.307006835938
            v 14.2842730710145 48.3028533074941 279.307006835938
            v 14.2842730710157 48.3028443243414 279.307006835938
            o cube
            f 1 2 3
            f 1 3 4
            f 2 5 6
            f 2 6 3
            f 5 7 8
            f 5 8 6
            f 7 1 4
            f 7 4 8
            f 4 3 6
            f 4 6 8
            f 7 5 2
            f 7 2 1
            """
        reader = GeoObjReader()

        # when
        geo_obj_file = reader.read_strings(input_str.split("\n"))

        # then
        self.assertTrue(geo_obj_file.is_geo_referenced())
        self.assertFalse(geo_obj_file.is_origin_based())
        self.assertEqual(len(geo_obj_file.objects), 1)
        self.assertEqual(geo_obj_file.objects[0].name, "cube")
        self.assertEqual(len(geo_obj_file.objects[0].faces), 12)
        self.assertEqual(len(geo_obj_file.vertices), 8)
