# flake8: noqa
# pylint: skip-file
import random

from geofiles.writer.base import BaseWriter
from geofiles.writer.kml_writer import KmlWriter
from tests.geofiles.writer.base_writer_test import BaseWriterTest


class TestKmlWriter(BaseWriterTest):
    def get_writer(self) -> BaseWriter:
        return KmlWriter()

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
        self.assertTrue("File must be opened in binary mode" in str(context.exception))

    def test_write3(self) -> None:
        data = self.get_cube()
        data.origin = [0, 0, 0]
        with self.assertRaises(Exception) as context:
            self._test_write(
                data, "cube" + self.get_writer().get_file_type(), write_binary=True
            )

        # then
        self.assertTrue(
            "Geo-referenced data must not be origin based" in str(context.exception)
        )

    def test_write4(self) -> None:
        data = self.get_cube()
        data.translation = [5, 5, 5]
        with self.assertRaises(Exception) as context:
            self._test_write(
                data, "cube" + self.get_writer().get_file_type(), write_binary=True
            )

        # then
        self.assertTrue("Given data contains translation" in str(context.exception))

    def test_write5(self) -> None:
        data = self.get_cube()
        data.rotation = [5, 5, 5]
        with self.assertRaises(Exception) as context:
            self._test_write(
                data, "cube" + self.get_writer().get_file_type(), write_binary=True
            )

        # then
        self.assertTrue("Given data contains rotation" in str(context.exception))

    def test_write6(self) -> None:
        data = self.get_cube()
        data.scaling = [5, 5, 5]
        with self.assertRaises(Exception) as context:
            self._test_write(
                data, "cube" + self.get_writer().get_file_type(), write_binary=True
            )

        # then
        self.assertTrue("Given data contains scale" in str(context.exception))

    def test_write7(self) -> None:
        data = self.get_cube()
        data.objects[0].scaling = [5, 5, 5]
        with self.assertRaises(Exception) as context:
            self._test_write(
                data, "cube" + self.get_writer().get_file_type(), write_binary=True
            )

        # then
        self.assertTrue(
            "KML does not support local object transformation information"
            in str(context.exception)
        )

    def test_write_to_string(self) -> None:
        # given
        data = self.get_cube()
        compare = """<?xml version='1.0' encoding='utf8'?>
<kml xmlns="http://www.opengis.net/kml/2.2"><Placemark><name>cube</name><Polygon><extrude>0</extrude><altitudeMode>absolute</altitudeMode><outerBoundaryIs><LinearRing><coordinates>
14.2842865755919 48.3028533074941 279.307006835938 
14.2842865755919 48.3028533074941 280.307006835938 
14.2842865755907 48.3028443243414 280.307006835938 
14.2842865755919 48.3028533074941 279.307006835938 </coordinates></LinearRing></outerBoundaryIs></Polygon><Polygon><extrude>0</extrude><altitudeMode>absolute</altitudeMode><outerBoundaryIs><LinearRing><coordinates>
14.2842865755919 48.3028533074941 279.307006835938 
14.2842865755907 48.3028443243414 280.307006835938 
14.2842865755907 48.3028443243414 279.307006835938 
14.2842865755919 48.3028533074941 279.307006835938 </coordinates></LinearRing></outerBoundaryIs></Polygon><Polygon><extrude>0</extrude><altitudeMode>absolute</altitudeMode><outerBoundaryIs><LinearRing><coordinates>
14.2842865755919 48.3028533074941 280.307006835938 
14.2842730710145 48.3028533074941 280.307006835938 
14.2842730710157 48.3028443243414 280.307006835938 
14.2842865755919 48.3028533074941 280.307006835938 </coordinates></LinearRing></outerBoundaryIs></Polygon><Polygon><extrude>0</extrude><altitudeMode>absolute</altitudeMode><outerBoundaryIs><LinearRing><coordinates>
14.2842865755919 48.3028533074941 280.307006835938 
14.2842730710157 48.3028443243414 280.307006835938 
14.2842865755907 48.3028443243414 280.307006835938 
14.2842865755919 48.3028533074941 280.307006835938 </coordinates></LinearRing></outerBoundaryIs></Polygon><Polygon><extrude>0</extrude><altitudeMode>absolute</altitudeMode><outerBoundaryIs><LinearRing><coordinates>
14.2842730710145 48.3028533074941 280.307006835938 
14.2842730710145 48.3028533074941 279.307006835938 
14.2842730710157 48.3028443243414 279.307006835938 
14.2842730710145 48.3028533074941 280.307006835938 </coordinates></LinearRing></outerBoundaryIs></Polygon><Polygon><extrude>0</extrude><altitudeMode>absolute</altitudeMode><outerBoundaryIs><LinearRing><coordinates>
14.2842730710145 48.3028533074941 280.307006835938 
14.2842730710157 48.3028443243414 279.307006835938 
14.2842730710157 48.3028443243414 280.307006835938 
14.2842730710145 48.3028533074941 280.307006835938 </coordinates></LinearRing></outerBoundaryIs></Polygon><Polygon><extrude>0</extrude><altitudeMode>absolute</altitudeMode><outerBoundaryIs><LinearRing><coordinates>
14.2842730710145 48.3028533074941 279.307006835938 
14.2842865755919 48.3028533074941 279.307006835938 
14.2842865755907 48.3028443243414 279.307006835938 
14.2842730710145 48.3028533074941 279.307006835938 </coordinates></LinearRing></outerBoundaryIs></Polygon><Polygon><extrude>0</extrude><altitudeMode>absolute</altitudeMode><outerBoundaryIs><LinearRing><coordinates>
14.2842730710145 48.3028533074941 279.307006835938 
14.2842865755907 48.3028443243414 279.307006835938 
14.2842730710157 48.3028443243414 279.307006835938 
14.2842730710145 48.3028533074941 279.307006835938 </coordinates></LinearRing></outerBoundaryIs></Polygon><Polygon><extrude>0</extrude><altitudeMode>absolute</altitudeMode><outerBoundaryIs><LinearRing><coordinates>
14.2842865755907 48.3028443243414 279.307006835938 
14.2842865755907 48.3028443243414 280.307006835938 
14.2842730710157 48.3028443243414 280.307006835938 
14.2842865755907 48.3028443243414 279.307006835938 </coordinates></LinearRing></outerBoundaryIs></Polygon><Polygon><extrude>0</extrude><altitudeMode>absolute</altitudeMode><outerBoundaryIs><LinearRing><coordinates>
14.2842865755907 48.3028443243414 279.307006835938 
14.2842730710157 48.3028443243414 280.307006835938 
14.2842730710157 48.3028443243414 279.307006835938 
14.2842865755907 48.3028443243414 279.307006835938 </coordinates></LinearRing></outerBoundaryIs></Polygon><Polygon><extrude>0</extrude><altitudeMode>absolute</altitudeMode><outerBoundaryIs><LinearRing><coordinates>
14.2842730710145 48.3028533074941 279.307006835938 
14.2842730710145 48.3028533074941 280.307006835938 
14.2842865755919 48.3028533074941 280.307006835938 
14.2842730710145 48.3028533074941 279.307006835938 </coordinates></LinearRing></outerBoundaryIs></Polygon><Polygon><extrude>0</extrude><altitudeMode>absolute</altitudeMode><outerBoundaryIs><LinearRing><coordinates>
14.2842730710145 48.3028533074941 279.307006835938 
14.2842865755919 48.3028533074941 280.307006835938 
14.2842865755919 48.3028533074941 279.307006835938 
14.2842730710145 48.3028533074941 279.307006835938 </coordinates></LinearRing></outerBoundaryIs></Polygon></Placemark></kml>"""
        rd = random.Random()
        rd.seed(42)
        # when
        string_rep = self.get_writer().write_to_string(
            data, write_binary=False, random_seed=rd.getrandbits(128)
        )

        # then
        self.assertEqual(string_rep, compare.strip())
