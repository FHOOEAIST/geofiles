from geofiles.writer.geo_json_writer import GeoJsonWriter
from tests.geofiles.writer.base_writer_test import BaseWriterTest


class TestGeoJsonWriter(BaseWriterTest):
    def get_writer(self):
        return GeoJsonWriter()

    def test_write(self):
        data = self.get_cube()
        self._test_write(data, "cube"+self.get_writer().get_file_type())
