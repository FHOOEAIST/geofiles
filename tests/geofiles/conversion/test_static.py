import unittest

from geofiles.conversion.static import get_epsg_4326, get_lon_lat, get_wgs_84


class TestStatic(unittest.TestCase):
    def test_get_wgs_84(self) -> None:
        # given
        ref = "urn:ogc:def:crs:OGC:2:84"
        # when
        wgs84 = get_wgs_84()

        # then
        self.assertEqual(wgs84, ref)

    def test_get_epsg_4326(self) -> None:
        # given
        ref = "urn:ogc:def:crs:EPSG::4326"

        # when
        epsg4326 = get_epsg_4326()

        # then
        self.assertEqual(epsg4326, ref)

    def test_get_lon_lat(self) -> None:
        # given
        epsg = get_epsg_4326()
        vertex = [48.3028533074941, 14.2842865755919, 279.307006835938]

        # when
        lon, lat = get_lon_lat(vertex, epsg)

        # then
        self.assertAlmostEqual(lon, vertex[1])
        self.assertAlmostEqual(lat, vertex[0])

    def test_get_lon_lat2(self) -> None:
        # given
        wgs = get_wgs_84()
        vertex = [48.3028533074941, 14.2842865755919, 279.307006835938]

        # when
        lon, lat = get_lon_lat(vertex, wgs)

        # then
        self.assertAlmostEqual(lon, vertex[0])
        self.assertAlmostEqual(lat, vertex[1])

    def test_get_lon_lat3(self) -> None:
        # given
        crs = "some_crs"
        vertex = [48.3028533074941, 14.2842865755919, 279.307006835938]

        # when
        with self.assertRaises(Exception) as context:
            get_lon_lat(vertex, crs)

        # then
        self.assertTrue("Not supported crs some_crs" in str(context.exception))
