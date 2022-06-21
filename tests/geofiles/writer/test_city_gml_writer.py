# flake8: noqa
# pylint: skip-file


from geofiles.writer.base import BaseWriter
from geofiles.writer.citygml_writer import CityGmlWriter
from tests.geofiles.writer.base_writer_test import BaseWriterTest


class TestCityGmlWriter(BaseWriterTest):
    def get_writer(self) -> BaseWriter:
        return CityGmlWriter()

    def test_write(self) -> None:
        data = self.get_cube()
        self._test_write(
            data, "cube" + self.get_writer().get_file_type(), write_binary=True
        )
