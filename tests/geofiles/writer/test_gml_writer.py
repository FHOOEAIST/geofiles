from typing import Optional

from geofiles.writer.base import BaseWriter
from geofiles.writer.gml_writer import GmlWriter
from tests.geofiles.writer.base_writer_test import BaseWriterTest


class TestGmlWriter(BaseWriterTest):
    def get_writer(self) -> Optional[BaseWriter]:
        return GmlWriter()

    def test_write(self) -> None:
        data = self.get_cube()
        self._test_write(
            data, "cube" + self.get_writer().get_file_type(), write_binary=True
        )

    def test_write2(self) -> None:
        data = self.get_cube()
        with self.assertRaises(Exception) as context:
            self._test_write(data, "cube" + self.get_writer().get_file_type())

        # then
        self.assertTrue(
            "File must be opened in binary mode for GML" in str(context.exception)
        )

    def test_write3(self) -> None:
        data = self.get_cube()
        data.origin = [0, 0, 0]
        with self.assertRaises(Exception) as context:
            self._test_write(data, "cube" + self.get_writer().get_file_type())

        # then
        self.assertTrue(
            "Geo-referenced data must not be origin based" in str(context.exception)
        )

    def test_write4(self) -> None:
        data = self.get_cube()
        data.translation = [5, 5, 5]
        with self.assertRaises(Exception) as context:
            self._test_write(data, "cube" + self.get_writer().get_file_type())

        # then
        self.assertTrue("Given data contains translation" in str(context.exception))

    def test_write5(self) -> None:
        data = self.get_cube()
        data.rotation = [5, 5, 5]
        with self.assertRaises(Exception) as context:
            self._test_write(data, "cube" + self.get_writer().get_file_type())

        # then
        self.assertTrue("Given data contains rotation" in str(context.exception))

    def test_write6(self) -> None:
        data = self.get_cube()
        data.scaling = [5, 5, 5]
        with self.assertRaises(Exception) as context:
            self._test_write(data, "cube" + self.get_writer().get_file_type())

        # then
        self.assertTrue("Given data contains scale" in str(context.exception))
