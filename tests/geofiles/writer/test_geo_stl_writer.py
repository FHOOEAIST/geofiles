from geofiles.writer.geo_stl_writer import GeoStlWriter
from tests.geofiles.writer.base_writer_test import BaseWriterTest


class TestGeoStlWriter(BaseWriterTest):
    def get_writer(self):
        return GeoStlWriter()

    def test_write(self):
        data = self.get_cube()
        self._test_write(data, "cube"+self.get_writer().get_file_type())