from geofiles.conversion.origin_converter import OriginConverter
from geofiles.writer.base import BaseWriter
from geofiles.writer.geo_ply_writer import GeoPlyWriter
from tests.geofiles.writer.base_writer_test import BaseWriterTest


class TestGeoPlyWriter(BaseWriterTest):
    def get_writer(self) -> BaseWriter:
        return GeoPlyWriter()

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
        converter = OriginConverter()
        origin = converter.to_origin(data)
        origin.update_extent()

        self._test_write(
            origin, "cube_origin_extent" + self.get_writer().get_file_type()
        )

    def test_write5(self) -> None:
        data = self.get_cube()
        data.objects += data.objects
        with self.assertRaises(Exception) as context:
            self._test_write(data, "cube" + self.get_writer().get_file_type())

        # then
        self.assertTrue(
            "GeoPLY can represent only one object. Minimize the data."
            in str(context.exception)
        )

    def test_write6(self) -> None:
        data = self.get_cube()
        data.objects[0].scaling = [5, 5, 5]
        with self.assertRaises(Exception) as context:
            self._test_write(data, "cube" + self.get_writer().get_file_type())

        # then
        self.assertTrue(
            "GeoPLY does not support local object transformation information"
            in str(context.exception)
        )

    def test_write7(self) -> None:
        data = self.get_cube()
        data.meta_information["tu"] = "inch"
        data.meta_information["ru"] = "rad"
        data.objects[0].meta_information["type"] = "GenericObject"
        converter = OriginConverter()
        origin = converter.to_origin(data)

        self._test_write(origin, "cube_meta" + self.get_writer().get_file_type())

    def test_write8(self) -> None:
        data = self.get_cube()
        data.meta_information["tu"] = "inch"
        data.meta_information["ru"] = "rad"
        data.meta_information["axis_ordering"] = ("x", "y", "z")
        data.objects[0].meta_information["type"] = "GenericObject"
        converter = OriginConverter()
        origin = converter.to_origin(data)

        self._test_write(origin, "cube_meta2" + self.get_writer().get_file_type())

    def test_write_local(self) -> None:
        data = self.get_local_cube()
        self._test_write(data, "cube.ply")

    def test_write_to_string(self) -> None:
        # given
        data = self.get_cube()
        compare = """geoply
format ascii 1.0
crs urn:ogc:def:crs:OGC:2:84
element vertex 8
property float x
property float y
property float z
element face  12
property list uchar int vertex_index
end_header
14.2842865755919 48.3028533074941 279.307006835938
14.2842865755919 48.3028533074941 280.307006835938
14.2842865755907 48.3028443243414 280.307006835938
14.2842865755907 48.3028443243414 279.307006835938
14.2842730710145 48.3028533074941 280.307006835938
14.2842730710157 48.3028443243414 280.307006835938
14.2842730710145 48.3028533074941 279.307006835938
14.2842730710157 48.3028443243414 279.307006835938
3 0 1 2
3 0 2 3
3 1 4 5
3 1 5 2
3 4 6 7
3 4 7 5
3 6 0 3
3 6 3 7
3 3 2 5
3 3 5 7
3 6 4 1
3 6 1 0
"""

        # when
        string_rep = self.get_writer().write_to_string(data)

        # then
        self.assertEqual(string_rep.strip(), compare.strip())
