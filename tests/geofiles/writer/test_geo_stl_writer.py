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
