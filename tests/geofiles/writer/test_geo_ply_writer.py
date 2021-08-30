from geofiles.conversion.origin_converter import OriginConverter
from geofiles.writer.geo_ply_writer import GeoPlyWriter
from tests.geofiles.writer.base_writer_test import BaseWriterTest


class TestGeoPlyWriter(BaseWriterTest):
    def get_writer(self):
        return GeoPlyWriter()

    def test_write(self):
        data = self.get_cube()
        self._test_write(data, "cube"+self.get_writer().get_file_type())

    def test_write2(self):
        data = self.get_cube()
        converter = OriginConverter()
        origin = converter.to_origin(data)

        self._test_write(origin, "cube_origin" + self.get_writer().get_file_type())

    def test_write3(self):
        data = self.get_cube()
        data.rotation = [90, 0, 0]
        data.scaling = [2, 2, 2]
        data.translation = [10, 50, 100]
        converter = OriginConverter()
        origin = converter.to_origin(data)

        self._test_write(origin, "cube_transformed" + self.get_writer().get_file_type())
