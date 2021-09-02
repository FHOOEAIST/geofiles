import os
import unittest

from geofiles.conversion.origin_converter import OriginConverter
from geofiles.domain.face import Face
from geofiles.domain.geo_object import GeoObject
from geofiles.domain.geo_object_file import GeoObjectFile
from geofiles.writer.base import BaseWriter


class BaseTest(unittest.TestCase):
    @staticmethod
    def get_cube(origin_based: bool = False) -> GeoObjectFile:
        """
        :param origin_based: flag if cube should be origin based
        :return: A sample GeoObjectFile representing a geo-referenced cube
        """
        res = GeoObjectFile()
        res.crs = "urn:ogc:def:crs:OGC:2:84"
        res.vertices = [
            [14.2842865755919, 48.3028533074941, 279.307006835938],
            [14.2842865755919, 48.3028533074941, 280.307006835938],
            [14.2842865755907, 48.3028443243414, 280.307006835938],
            [14.2842865755907, 48.3028443243414, 279.307006835938],
            [14.2842730710145, 48.3028533074941, 280.307006835938],
            [14.2842730710157, 48.3028443243414, 280.307006835938],
            [14.2842730710145, 48.3028533074941, 279.307006835938],
            [14.2842730710157, 48.3028443243414, 279.307006835938],
        ]
        geoobject = GeoObject()
        geoobject.name = "cube"
        f1 = Face()
        f1.indices = [1, 2, 3]
        f2 = Face()
        f2.indices = [1, 3, 4]
        f3 = Face()
        f3.indices = [2, 5, 6]
        f4 = Face()
        f4.indices = [2, 6, 3]
        f5 = Face()
        f5.indices = [5, 7, 8]
        f6 = Face()
        f6.indices = [5, 8, 6]
        f7 = Face()
        f7.indices = [7, 1, 4]
        f8 = Face()
        f8.indices = [7, 4, 8]
        f9 = Face()
        f9.indices = [4, 3, 6]
        f10 = Face()
        f10.indices = [4, 6, 8]
        f11 = Face()
        f11.indices = [7, 5, 2]
        f12 = Face()
        f12.indices = [7, 2, 1]

        faces = [f1, f2, f3, f4, f5, f6, f7, f8, f9, f10, f11, f12]

        geoobject.faces = faces

        res.objects = [geoobject]

        if origin_based:
            converter = OriginConverter()
            return converter.to_origin(res)

        return res

    @classmethod
    def get_local_cube(cls) -> GeoObjectFile:
        """
        :return: A local geometry example of a cube without a referenced coordinate system
        """
        res = cls.get_cube()
        res.crs = None
        res.vertices = [
            [-0.5, -0.5, 0.5],
            [-0.5, -0.5, -0.5],
            [-0.5, 0.5, -0.5],
            [-0.5, 0.5, 0.5],
            [0.5, -0.5, -0.5],
            [0.5, 0.5, -0.5],
            [0.5, -0.5, 0.5],
            [0.5, 0.5, 0.5],
        ]

        return res

    def compare_with_cube(self, geo_obj_file: GeoObjectFile) -> None:
        """
        Compares the given GeoObjectFile with the cube
        :param geo_obj_file: to be compared
        :return: None
        """
        cube = self.get_cube()
        self.assertTrue(geo_obj_file.is_geo_referenced())
        self.assertFalse(geo_obj_file.is_origin_based())
        self.assertEqual(len(geo_obj_file.objects), 1)
        self.assertEqual(len(geo_obj_file.objects[0].faces), 12)
        self.assertEqual(len(geo_obj_file.vertices), 8)
        self.assertEqual(geo_obj_file.crs, "urn:ogc:def:crs:OGC:2:84")
        self.compare_geo_obj_files(cube, geo_obj_file)

    def compare_geo_obj_files(self, file1: GeoObjectFile, file2: GeoObjectFile):
        """
        Compares the given GeoObjectFiles according to their faces and vertices
        """
        for obj_idx, object in enumerate(file1.objects):
            for idx, face in enumerate(object.faces):
                for inneridx, i in enumerate(face.indices):
                    self.assertEqual(
                        int(i), int(file2.objects[obj_idx].faces[idx].indices[inneridx])
                    )

        for idx, vertex in enumerate(file1.vertices):
            self.assertAlmostEqual(float(vertex[0]), file2.vertices[idx][0])
            self.assertAlmostEqual(float(vertex[1]), file2.vertices[idx][1])
            self.assertAlmostEqual(float(vertex[2]), file2.vertices[idx][2])

    @staticmethod
    def get_ressource_file(filename: str) -> str:
        """
        Gets a file in the ressource folder
        :param filename: name of the file
        :return: full path to the file
        """
        cwd = os.getcwd()
        idx = cwd.find("tests")
        cwd = cwd[:idx]
        if not cwd.endswith(os.sep):
            cwd = cwd[: idx + 1]
        return os.path.join(os.path.join(cwd, "ressources"), filename)

    @classmethod
    def get_test_file(cls, writer: BaseWriter) -> str:
        return cls.get_ressource_file("test" + writer.get_file_type())
