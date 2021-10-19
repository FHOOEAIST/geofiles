import json

from geofiles.reader.city_json_reader import CityJsonReader
from tests.geofiles.base_test import BaseTest


class TestCityJsonReader(BaseTest):
    def test_read(self) -> None:
        # given
        file = self.get_ressource_file("cube.city.json")
        reader = CityJsonReader()
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

    def test_read_string(self) -> None:
        # given
        file = self.get_ressource_file("cube.city.json")
        with open(file) as json_file:
            j = json.load(json_file)
            reader = CityJsonReader()
            cube = self.get_cube()

            # when
            geo_obj_file = reader.read_string(json.dumps(j))

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

    def test_read_string2(self) -> None:
        # given
        file = self.get_ressource_file("cube.city.json")
        with open(file) as json_file:
            j = json.load(json_file)
            del j["metadata"]
            reader = CityJsonReader()

            # when
            with self.assertRaises(Exception) as context:
                reader.read_string(json.dumps(j))

            # then
            self.assertTrue(
                "No metadata defined (at least reference system is required)"
                in str(context.exception)
            )

    def test_read_string3(self) -> None:
        # given
        file = self.get_ressource_file("cube.city.json")
        with open(file) as json_file:
            j = json.load(json_file)
            metadata = j["metadata"]
            metadata["yo"] = "test"
            del metadata["referenceSystem"]
            reader = CityJsonReader()

            # when
            with self.assertRaises(Exception) as context:
                reader.read_string(json.dumps(j))

            # then
            self.assertTrue(
                "Unknown reference system in input file." in str(context.exception)
            )

    def test_read_string4(self) -> None:
        # given
        file = self.get_ressource_file("cube.city.json")
        with open(file) as json_file:
            j = json.load(json_file)
            del j["vertices"]
            reader = CityJsonReader()

            # when
            with self.assertRaises(Exception) as context:
                reader.read_string(json.dumps(j))

            # then
            self.assertTrue(
                "Undefined vertices in input file." in str(context.exception)
            )

    def test_read_string5(self) -> None:
        # given
        file = self.get_ressource_file("cube.city.json")
        with open(file) as json_file:
            j = json.load(json_file)
            del j["CityObjects"]
            reader = CityJsonReader()

            # when
            with self.assertRaises(Exception) as context:
                reader.read_string(json.dumps(j))

            # then
            self.assertTrue("No city objects defined" in str(context.exception))
