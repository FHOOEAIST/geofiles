from geofiles.writer.gml_writer import GmlWriter
from tests.geofiles.writer.base_writer_test import BaseWriterTest


class TestGmlWriter(BaseWriterTest):
    def get_writer(self):
        return GmlWriter()

    def test_write(self):
        data = self.get_cube()
        self._test_write(data, "cube"+self.get_writer().get_file_type(), write_binary=True)