from geofiles.writer.geo_off_writer import GeoOffWriter
from tests.geofiles.writer.base_writer_test import BaseWriterTest


class TestGeoOffWriter(BaseWriterTest):
    def get_writer(self):
        return GeoOffWriter()

    def test_write(self):
        data = self.get_cube()
        self._test_write(data, "cube"+self.get_writer().get_file_type())