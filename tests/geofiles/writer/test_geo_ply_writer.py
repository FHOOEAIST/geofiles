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

    def test_write_local(self) -> None:
        data = self.get_local_cube()
        self._test_write(data, "cube.ply")
