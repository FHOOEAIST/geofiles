# flake8: noqa
# pylint: skip-file
from geofiles.conversion.origin_converter import OriginConverter
from geofiles.writer.base import BaseWriter
from geofiles.writer.geo_stl_writer import GeoStlWriter
from tests.geofiles.writer.base_writer_test import BaseWriterTest


class TestGeoStlWriter(BaseWriterTest):
    def get_writer(self) -> BaseWriter:
        return GeoStlWriter()

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
        data.translation = [5, 5, 5]
        with self.assertRaises(Exception) as context:
            self._test_write(data, "cube" + self.get_writer().get_file_type())

        # then
        self.assertTrue("Given data contains translation" in str(context.exception))

    def test_write4(self) -> None:
        data = self.get_cube()
        data.rotation = [5, 5, 5]
        with self.assertRaises(Exception) as context:
            self._test_write(data, "cube" + self.get_writer().get_file_type())

        # then
        self.assertTrue("Given data contains rotation" in str(context.exception))

    def test_write5(self) -> None:
        data = self.get_cube()
        data.scaling = [5, 5, 5]
        with self.assertRaises(Exception) as context:
            self._test_write(data, "cube" + self.get_writer().get_file_type())

        # then
        self.assertTrue("Given data contains scale" in str(context.exception))

    def test_write6(self) -> None:
        data = self.get_cube()
        data.objects += data.objects
        with self.assertRaises(Exception) as context:
            self._test_write(data, "cube" + self.get_writer().get_file_type())

        # then
        self.assertTrue(
            "GeoSTL can represent only one object. Minimize the data."
            in str(context.exception)
        )

    def test_write7(self) -> None:
        data = self.get_cube()
        data.objects[0].scaling = [5, 5, 5]
        with self.assertRaises(Exception) as context:
            self._test_write(data, "cube" + self.get_writer().get_file_type())

        # then
        self.assertTrue(
            "GeoSTL does not support local object transformation information"
            in str(context.exception)
        )

    def test_write_local(self) -> None:
        data = self.get_local_cube()
        self._test_write(data, "cube.stl")

    def test_write_to_string(self) -> None:
        # given
        data = self.get_cube()
        compare = """geosolid urn:ogc:def:crs:OGC:2:84  
 facet
  outer loop
   vertex 14.2842865755919 48.3028533074941 279.307006835938
   vertex 14.2842865755919 48.3028533074941 280.307006835938
   vertex 14.2842865755907 48.3028443243414 280.307006835938
  endloop
 endfacet
 facet
  outer loop
   vertex 14.2842865755919 48.3028533074941 279.307006835938
   vertex 14.2842865755907 48.3028443243414 280.307006835938
   vertex 14.2842865755907 48.3028443243414 279.307006835938
  endloop
 endfacet
 facet
  outer loop
   vertex 14.2842865755919 48.3028533074941 280.307006835938
   vertex 14.2842730710145 48.3028533074941 280.307006835938
   vertex 14.2842730710157 48.3028443243414 280.307006835938
  endloop
 endfacet
 facet
  outer loop
   vertex 14.2842865755919 48.3028533074941 280.307006835938
   vertex 14.2842730710157 48.3028443243414 280.307006835938
   vertex 14.2842865755907 48.3028443243414 280.307006835938
  endloop
 endfacet
 facet
  outer loop
   vertex 14.2842730710145 48.3028533074941 280.307006835938
   vertex 14.2842730710145 48.3028533074941 279.307006835938
   vertex 14.2842730710157 48.3028443243414 279.307006835938
  endloop
 endfacet
 facet
  outer loop
   vertex 14.2842730710145 48.3028533074941 280.307006835938
   vertex 14.2842730710157 48.3028443243414 279.307006835938
   vertex 14.2842730710157 48.3028443243414 280.307006835938
  endloop
 endfacet
 facet
  outer loop
   vertex 14.2842730710145 48.3028533074941 279.307006835938
   vertex 14.2842865755919 48.3028533074941 279.307006835938
   vertex 14.2842865755907 48.3028443243414 279.307006835938
  endloop
 endfacet
 facet
  outer loop
   vertex 14.2842730710145 48.3028533074941 279.307006835938
   vertex 14.2842865755907 48.3028443243414 279.307006835938
   vertex 14.2842730710157 48.3028443243414 279.307006835938
  endloop
 endfacet
 facet
  outer loop
   vertex 14.2842865755907 48.3028443243414 279.307006835938
   vertex 14.2842865755907 48.3028443243414 280.307006835938
   vertex 14.2842730710157 48.3028443243414 280.307006835938
  endloop
 endfacet
 facet
  outer loop
   vertex 14.2842865755907 48.3028443243414 279.307006835938
   vertex 14.2842730710157 48.3028443243414 280.307006835938
   vertex 14.2842730710157 48.3028443243414 279.307006835938
  endloop
 endfacet
 facet
  outer loop
   vertex 14.2842730710145 48.3028533074941 279.307006835938
   vertex 14.2842730710145 48.3028533074941 280.307006835938
   vertex 14.2842865755919 48.3028533074941 280.307006835938
  endloop
 endfacet
 facet
  outer loop
   vertex 14.2842730710145 48.3028533074941 279.307006835938
   vertex 14.2842865755919 48.3028533074941 280.307006835938
   vertex 14.2842865755919 48.3028533074941 279.307006835938
  endloop
 endfacet
endgeosolid
"""

        # when
        string_rep = self.get_writer().write_to_string(data)

        # then
        self.assertEqual(string_rep.strip(), compare.strip())
