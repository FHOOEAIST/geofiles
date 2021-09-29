# flake8: noqa
import copy

from geofiles.conversion.origin_converter import OriginConverter
from geofiles.writer.base import BaseWriter
from geofiles.writer.geo_vrml_writer import GeoVrmlWriter
from tests.geofiles.writer.base_writer_test import BaseWriterTest


class TestGeoVrmlWriter(BaseWriterTest):
    def get_writer(self) -> BaseWriter:
        return GeoVrmlWriter()

    def test_write(self) -> None:
        data = self.get_cube()
        self._test_write(data, "cube" + self.get_writer().get_file_type())

    def test_write2(self) -> None:
        data = self.get_cube()
        converter = OriginConverter()
        origin = converter.to_origin(data)

        self._test_write(origin, "cube_origin" + self.get_writer().get_file_type())

    def test_write3(self) -> None:
        data = self.get_cube()
        data.rotation = [90, 0, 0]
        data.scaling = [2, 2, 2]
        data.translation = [10, 50, 100]
        converter = OriginConverter()
        origin = converter.to_origin(data)

        self._test_write(origin, "cube_transformed" + self.get_writer().get_file_type())

    def test_write4(self) -> None:
        data = self.get_cube()
        data.rotation = [90, 0, 0]
        data.scaling = [2, 2, 2]
        data.translation = [10, 50, 100]

        data.objects.append(copy.deepcopy(data.objects[0]))
        data.objects[0].scaling = [5, 5, 5]
        data.objects[1].translation = [50, 20, 30]

        converter = OriginConverter()
        origin = converter.to_origin(data)

        self._test_write(
            origin, "cube_transformed_local" + self.get_writer().get_file_type()
        )

    def test_write_to_string(self) -> None:
        # given
        data = self.get_cube()
        compare = """#VRML V2.0 utf8
EXTERNPROTO GeoCoordinate [
 field SFNode geoOrigin # NULL
 field MFString geoSystem # [ "GDC" ]
 field MFString point # []
 field MFString point # []
] [ "urn:web3d:geovrml:1.0/protos/GeoCoordinate.wrl"
 "file:///C|/Program%20Files/GeoVRML/1.0/protos/GeoCoordinate.wrl"
 "http://www.geovrml.org/1.0/protos/GeoCoordinate.wrl" ]
DEF OBJECT-0 Shape {
   geometry IndexedFaceSet {
      coord GeoCoordinate {
         geoSystem [ "GDC" ]
         point [
            14.2842865755919 48.3028533074941 279.307006835938 
            14.2842865755919 48.3028533074941 280.307006835938 
            14.2842865755907 48.3028443243414 280.307006835938 
            14.2842865755919 48.3028533074941 279.307006835938 
            14.2842865755907 48.3028443243414 280.307006835938 
            14.2842865755907 48.3028443243414 279.307006835938 
            14.2842865755919 48.3028533074941 280.307006835938 
            14.2842730710145 48.3028533074941 280.307006835938 
            14.2842730710157 48.3028443243414 280.307006835938 
            14.2842865755919 48.3028533074941 280.307006835938 
            14.2842730710157 48.3028443243414 280.307006835938 
            14.2842865755907 48.3028443243414 280.307006835938 
            14.2842730710145 48.3028533074941 280.307006835938 
            14.2842730710145 48.3028533074941 279.307006835938 
            14.2842730710157 48.3028443243414 279.307006835938 
            14.2842730710145 48.3028533074941 280.307006835938 
            14.2842730710157 48.3028443243414 279.307006835938 
            14.2842730710157 48.3028443243414 280.307006835938 
            14.2842730710145 48.3028533074941 279.307006835938 
            14.2842865755919 48.3028533074941 279.307006835938 
            14.2842865755907 48.3028443243414 279.307006835938 
            14.2842730710145 48.3028533074941 279.307006835938 
            14.2842865755907 48.3028443243414 279.307006835938 
            14.2842730710157 48.3028443243414 279.307006835938 
            14.2842865755907 48.3028443243414 279.307006835938 
            14.2842865755907 48.3028443243414 280.307006835938 
            14.2842730710157 48.3028443243414 280.307006835938 
            14.2842865755907 48.3028443243414 279.307006835938 
            14.2842730710157 48.3028443243414 280.307006835938 
            14.2842730710157 48.3028443243414 279.307006835938 
            14.2842730710145 48.3028533074941 279.307006835938 
            14.2842730710145 48.3028533074941 280.307006835938 
            14.2842865755919 48.3028533074941 280.307006835938 
            14.2842730710145 48.3028533074941 279.307006835938 
            14.2842865755919 48.3028533074941 280.307006835938 
            14.2842865755919 48.3028533074941 279.307006835938 
         ]
      }
      coordIndex [0 1 2 -1, 0 2 3 -1, 1 4 5 -1, 1 5 2 -1, 4 6 7 -1, 4 7 5 -1, 6 0 3 -1, 6 3 7 -1, 3 2 5 -1, 3 5 7 -1, 6 4 1 -1, 6 1 0 -1]
   }
}"""

        # when
        string_rep = self.get_writer().write_to_string(data)

        # then
        self.assertEqual(string_rep.strip(), compare.strip())
