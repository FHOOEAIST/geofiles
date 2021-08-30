from geofiles.reader.geo_obj_reader import GeoObjReader
from tests.geofiles.base_test import BaseTest


class TestGeoObjReader(BaseTest):
    def test_read(self):
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

    def test_read2(self):
        # given
        file = self.get_ressource_file("local.obj")
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

    def test_read3(self):
        # given
        file = self.get_ressource_file("cube_origin.geoobj")
        reader = GeoObjReader()

        # when
        geo_obj_file = reader.read(file)

        # then
        self.assertEqual(
            geo_obj_file.origin,
            ["14.2842798233032", "48.30284881591775", "279.807006835938"],
        )

    def test_read4(self):
        # given
        file = self.get_ressource_file("cube_transformed.geoobj")
        reader = GeoObjReader()

        # when
        geo_obj_file = reader.read(file)

        # then
        self.assertEqual(
            geo_obj_file.origin,
            ["14.2842798233032", "48.30284881591775", "279.807006835938"],
        )
        self.assertEqual(geo_obj_file.translation, ["10", "50", "100"])
        self.assertEqual(geo_obj_file.scaling, ["2", "2", "2"])
        self.assertEqual(geo_obj_file.rotation, ["90", "0", "0"])
