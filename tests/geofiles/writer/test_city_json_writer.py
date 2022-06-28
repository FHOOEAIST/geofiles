# pylint: skip-file
from geofiles.conversion.origin_converter import OriginConverter
from geofiles.writer.base import BaseWriter
from geofiles.writer.city_json_writer import CityJsonVersion, CityJsonWriter
from tests.geofiles.writer.base_writer_test import BaseWriterTest


class TestCityJsonWriter(BaseWriterTest):
    def get_writer(self) -> BaseWriter:
        return CityJsonWriter()

    def test_write(self) -> None:
        data = self.get_cube()
        data.scaling = [1, 2, 3]
        data.translation = [4, 5, 6]
        self._test_write(data, "cube1-1" + self.get_writer().get_file_type())

    def test_write2(self) -> None:
        data = self.get_cube()
        writer = CityJsonWriter(CityJsonVersion.V1_0)
        self._test_write(
            data, "cube1-0" + self.get_writer().get_file_type(), writer_to_use=writer
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
        data.rotation = [5, 5, 5]
        with self.assertRaises(Exception) as context:
            self._test_write(data, "cube" + self.get_writer().get_file_type())

        # then
        self.assertTrue(
            "CityJSON does not support rotational information" in str(context.exception)
        )

    def test_write5(self) -> None:
        data = self.get_cube()
        data.objects[0].scaling = [5, 5, 5]
        writer = CityJsonWriter(CityJsonVersion.V1_0)
        with self.assertRaises(Exception) as context:
            self._test_write(
                data, "cube" + self.get_writer().get_file_type(), writer_to_use=writer
            )

        # then
        self.assertTrue(
            "CityJSON does not support local object transformation information"
            in str(context.exception)
        )

    def test_write6(self) -> None:
        data = self.get_cube()
        converter = OriginConverter()
        origin = converter.to_origin(data)
        origin.update_extent()

        self._test_write(
            origin,
            "cube_origin_extent" + self.get_writer().get_file_type(),
            writer_to_use=CityJsonWriter(use_transform_for_origin=True),
        )

    def test_write7(self) -> None:
        data = self.get_cube()
        data.translation = [5, 5, 5]
        converter = OriginConverter()
        origin = converter.to_origin(data)
        origin.update_extent()

        self._test_write(
            origin,
            "cube_origin_extent2" + self.get_writer().get_file_type(),
            writer_to_use=CityJsonWriter(use_transform_for_origin=True),
        )

    def test_write_to_string(self) -> None:
        # given
        data = self.get_cube()
        compare = '{"type": "CityJSON", "version": "1.1", "transform": {"scale": [1.0, 1.0, 1.0], "translate": [0.0, 0.0, 0.0]}, "metadata": {"referenceSystem": "urn:ogc:def:crs:OGC:2:84"}, "CityObjects": {"cube": {"type": "GenericCityObject", "geometry": [{"type": "MultiSurface", "lod": 1, "boundaries": [[[0, 1, 2]], [[0, 2, 3]], [[1, 4, 5]], [[1, 5, 2]], [[4, 6, 7]], [[4, 7, 5]], [[6, 0, 3]], [[6, 3, 7]], [[3, 2, 5]], [[3, 5, 7]], [[6, 4, 1]], [[6, 1, 0]]]}]}}, "vertices": [[14.2842865755919, 48.3028533074941, 279.307006835938], [14.2842865755919, 48.3028533074941, 280.307006835938], [14.2842865755907, 48.3028443243414, 280.307006835938], [14.2842865755907, 48.3028443243414, 279.307006835938], [14.2842730710145, 48.3028533074941, 280.307006835938], [14.2842730710157, 48.3028443243414, 280.307006835938], [14.2842730710145, 48.3028533074941, 279.307006835938], [14.2842730710157, 48.3028443243414, 279.307006835938]]}'

        # when
        string_rep = self.get_writer().write_to_string(data)

        # then
        self.assertEqual(string_rep.strip(), compare.strip())
