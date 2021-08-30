from geofiles.writer.city_json_writer import CityJsonWriter
from tests.geofiles.writer.base_writer_test import BaseWriterTest


class TestCityJsonWriter(BaseWriterTest):
    def get_writer(self):
        return CityJsonWriter()

    def test_write(self):
        data = self.get_cube()
        self._test_write(data, "cube"+self.get_writer().get_file_type())
