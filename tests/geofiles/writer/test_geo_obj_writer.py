from geofiles.conversion.origin_converter import OriginConverter
from geofiles.writer.geo_obj_writer import GeoObjWriter
from tests.geofiles.writer.base_writer_test import BaseWriterTest


class TestGeoObjWriter(BaseWriterTest):
    def get_writer(self):
        return GeoObjWriter()

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
