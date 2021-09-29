from geofiles.conversion.origin_converter import OriginConverter
from geofiles.writer.base import BaseWriter
from geofiles.writer.geo_obj_writer import GeoObjWriter
from tests.geofiles.writer.base_writer_test import BaseWriterTest


class TestGeoObjWriter(BaseWriterTest):
    def get_writer(self) -> BaseWriter:
        return GeoObjWriter()

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
        data.objects[0].rotation = [90, 0, 0]
        data.objects[0].scaling = [2, 2, 2]
        data.objects[0].translation = [10, 50, 100]
        converter = OriginConverter()
        origin = converter.to_origin(data)

        self._test_write(
            origin, "cube_transformed_local" + self.get_writer().get_file_type()
        )

    def test_write_local(self) -> None:
        data = self.get_local_cube()
        self._test_write(data, "cube.obj")

    def test_write_to_string(self) -> None:
        # given
        data = self.get_cube()
        compare = """
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
f 7 2 1"""

        # when
        string_rep = self.get_writer().write_to_string(data)

        # then
        self.assertEqual(string_rep.strip(), compare.strip())
