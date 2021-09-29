# pylint: skip-file
from geofiles.writer.base import BaseWriter
from geofiles.writer.geo_json_writer import GeoJsonWriter
from tests.geofiles.writer.base_writer_test import BaseWriterTest


class TestGeoJsonWriter(BaseWriterTest):
    def get_writer(self) -> BaseWriter:
        return GeoJsonWriter()

    def test_write(self) -> None:
        data = self.get_cube()
        self._test_write(data, "cube" + self.get_writer().get_file_type())

    def test_write2(self) -> None:
        data = self.get_cube()
        data.origin = [0, 0, 0]
        with self.assertRaises(Exception) as context:
            self._test_write(data, "cube" + self.get_writer().get_file_type())

        # then
        self.assertTrue(
            "Geo-referenced data must not be origin based" in str(context.exception)
        )

    def test_write3(self) -> None:
        data = self.get_cube()
        data.translation = [5, 5, 5]
        with self.assertRaises(Exception) as context:
            self._test_write(data, "cube" + self.get_writer().get_file_type())

        # then
        self.assertTrue("Given data contains translation" in str(context.exception))

    def test_write4(self) -> None:
        data = self.get_cube()
        data.rotation = [5, 5, 5]
        with self.assertRaises(Exception) as context:
            self._test_write(data, "cube" + self.get_writer().get_file_type())

        # then
        self.assertTrue("Given data contains rotation" in str(context.exception))

    def test_write5(self) -> None:
        data = self.get_cube()
        data.scaling = [5, 5, 5]
        with self.assertRaises(Exception) as context:
            self._test_write(data, "cube" + self.get_writer().get_file_type())

        # then
        self.assertTrue("Given data contains scale" in str(context.exception))

    def test_write6(self) -> None:
        data = self.get_cube()
        data.objects[0].scaling = [5, 5, 5]
        with self.assertRaises(Exception) as context:
            self._test_write(data, "cube" + self.get_writer().get_file_type())

        # then
        self.assertTrue(
            "GeoJSON does not support local object transformation information"
            in str(context.exception)
        )

    def test_write_to_string(self) -> None:
        # given
        data = self.get_cube()
        compare = '{"type": "FeatureCollection", "features": [{"type": "MultiPolygon", "coordinates": [[[[14.2842865755919, 48.3028533074941, 279.307006835938], [14.2842865755919, 48.3028533074941, 280.307006835938], [14.2842865755907, 48.3028443243414, 280.307006835938], [14.2842865755919, 48.3028533074941, 279.307006835938]]], [[[14.2842865755919, 48.3028533074941, 279.307006835938], [14.2842865755907, 48.3028443243414, 280.307006835938], [14.2842865755907, 48.3028443243414, 279.307006835938], [14.2842865755919, 48.3028533074941, 279.307006835938]]], [[[14.2842865755919, 48.3028533074941, 280.307006835938], [14.2842730710145, 48.3028533074941, 280.307006835938], [14.2842730710157, 48.3028443243414, 280.307006835938], [14.2842865755919, 48.3028533074941, 280.307006835938]]], [[[14.2842865755919, 48.3028533074941, 280.307006835938], [14.2842730710157, 48.3028443243414, 280.307006835938], [14.2842865755907, 48.3028443243414, 280.307006835938], [14.2842865755919, 48.3028533074941, 280.307006835938]]], [[[14.2842730710145, 48.3028533074941, 280.307006835938], [14.2842730710145, 48.3028533074941, 279.307006835938], [14.2842730710157, 48.3028443243414, 279.307006835938], [14.2842730710145, 48.3028533074941, 280.307006835938]]], [[[14.2842730710145, 48.3028533074941, 280.307006835938], [14.2842730710157, 48.3028443243414, 279.307006835938], [14.2842730710157, 48.3028443243414, 280.307006835938], [14.2842730710145, 48.3028533074941, 280.307006835938]]], [[[14.2842730710145, 48.3028533074941, 279.307006835938], [14.2842865755919, 48.3028533074941, 279.307006835938], [14.2842865755907, 48.3028443243414, 279.307006835938], [14.2842730710145, 48.3028533074941, 279.307006835938]]], [[[14.2842730710145, 48.3028533074941, 279.307006835938], [14.2842865755907, 48.3028443243414, 279.307006835938], [14.2842730710157, 48.3028443243414, 279.307006835938], [14.2842730710145, 48.3028533074941, 279.307006835938]]], [[[14.2842865755907, 48.3028443243414, 279.307006835938], [14.2842865755907, 48.3028443243414, 280.307006835938], [14.2842730710157, 48.3028443243414, 280.307006835938], [14.2842865755907, 48.3028443243414, 279.307006835938]]], [[[14.2842865755907, 48.3028443243414, 279.307006835938], [14.2842730710157, 48.3028443243414, 280.307006835938], [14.2842730710157, 48.3028443243414, 279.307006835938], [14.2842865755907, 48.3028443243414, 279.307006835938]]], [[[14.2842730710145, 48.3028533074941, 279.307006835938], [14.2842730710145, 48.3028533074941, 280.307006835938], [14.2842865755919, 48.3028533074941, 280.307006835938], [14.2842730710145, 48.3028533074941, 279.307006835938]]], [[[14.2842730710145, 48.3028533074941, 279.307006835938], [14.2842865755919, 48.3028533074941, 280.307006835938], [14.2842865755919, 48.3028533074941, 279.307006835938], [14.2842730710145, 48.3028533074941, 279.307006835938]]]]}]}'

        # when
        string_rep = self.get_writer().write_to_string(data)

        # then
        self.assertEqual(string_rep.strip(), compare.strip())
