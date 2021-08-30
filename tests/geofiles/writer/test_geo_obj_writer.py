from geofiles.writer.geo_obj_writer import GeoObjWriter
from tests.geofiles.writer.base_writer_test import BaseWriterTest


class TestGeoObjWriter(BaseWriterTest):
    def get_writer(self):
        return GeoObjWriter()

    def test_write(self):
        data = self.get_cube()
        self._test_write(data, "cube"+self.get_writer().get_file_type())
