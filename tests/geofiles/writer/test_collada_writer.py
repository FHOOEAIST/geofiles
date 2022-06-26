# flake8: noqa
# pylint: skip-file
import datetime

from geofiles.writer.base import BaseWriter
from geofiles.writer.collada_writer import ColladaWriter
from tests.geofiles.writer.base_writer_test import BaseWriterTest


class TestColladaWriter(BaseWriterTest):
    def get_writer(self) -> BaseWriter:
        return ColladaWriter(datetime.datetime(2022, 6, 26, 11, 11, 11))

    def test_write(self) -> None:
        data = self.get_cube()
        self._test_write(
            data, "cube" + self.get_writer().get_file_type(), write_binary=True
        )
