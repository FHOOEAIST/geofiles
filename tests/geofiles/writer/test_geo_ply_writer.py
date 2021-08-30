from geofiles.writer.geo_ply_writer import GeoPlyWriter
from tests.geofiles.writer.base_writer_test import BaseWriterTest


class TestGeoPlyWriter(BaseWriterTest):
    def get_writer(self):
        return GeoPlyWriter()

    def test_write(self):
        data = self.get_cube()
        self._test_write(data, "cube"+self.get_writer().get_file_type())