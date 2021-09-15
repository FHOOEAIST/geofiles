from geofiles.domain.geo_object import GeoObject
from tests.geofiles.base_test import BaseTest


class TestGeoObject(BaseTest):
    def test_contains_scaling(self) -> None:
        # given
        geoobject = GeoObject()

        # when
        res = geoobject.contains_scaling()

        # then
        self.assertFalse(res)

    def test_contains_scaling2(self) -> None:
        # given
        geoobject = GeoObject()
        geoobject.scaling = [1, 1, 1]

        # when
        res = geoobject.contains_scaling()

        # then
        self.assertFalse(res)

    def test_contains_scaling3(self) -> None:
        # given
        geoobject = GeoObject()
        geoobject.scaling = [1.0, 1.0, 1.0]

        # when
        res = geoobject.contains_scaling()

        # then
        self.assertFalse(res)

    def test_contains_scaling4(self) -> None:
        # given
        geoobject = GeoObject()
        geoobject.scaling = []

        # when
        res = geoobject.contains_scaling()

        # then
        self.assertFalse(res)

    def test_contains_scaling5(self) -> None:
        # given
        geoobject = GeoObject()
        geoobject.scaling = [5.0, 1.0, 1.0]

        # when
        res = geoobject.contains_scaling()

        # then
        self.assertTrue(res)

    def test_contains_rotation(self) -> None:
        # given
        geoobject = GeoObject()

        # when
        res = geoobject.contains_rotation()

        # then
        self.assertFalse(res)

    def test_contains_rotation2(self) -> None:
        # given
        geoobject = GeoObject()
        geoobject.rotation = [0, 0, 0]

        # when
        res = geoobject.contains_rotation()

        # then
        self.assertFalse(res)

    def test_contains_rotation3(self) -> None:
        # given
        geoobject = GeoObject()
        geoobject.rotation = [0.0, 0.0, 0.0]

        # when
        res = geoobject.contains_rotation()

        # then
        self.assertFalse(res)

    def test_contains_rotation4(self) -> None:
        # given
        geoobject = GeoObject()
        geoobject.rotation = [5.0, 1.0, 1.0]

        # when
        res = geoobject.contains_rotation()

        # then
        self.assertTrue(res)

    def test_contains_rotation5(self) -> None:
        # given
        geoobject = GeoObject()
        geoobject.rotation = []

        # when
        res = geoobject.contains_rotation()

        # then
        self.assertFalse(res)

    def test_contains_translation(self) -> None:
        # given
        geoobject = GeoObject()

        # when
        res = geoobject.contains_translation()

        # then
        self.assertFalse(res)

    def test_contains_translation2(self) -> None:
        # given
        geoobject = GeoObject()
        geoobject.translation = [0, 0, 0]

        # when
        res = geoobject.contains_translation()

        # then
        self.assertFalse(res)

    def test_contains_translation3(self) -> None:
        # given
        geoobject = GeoObject()
        geoobject.translation = [0.0, 0.0, 0.0]

        # when
        res = geoobject.contains_translation()

        # then
        self.assertFalse(res)

    def test_contains_translation4(self) -> None:
        # given
        geoobject = GeoObject()
        geoobject.translation = []

        # when
        res = geoobject.contains_translation()

        # then
        self.assertFalse(res)

    def test_contains_translation5(self) -> None:
        # given
        geoobject = GeoObject()
        geoobject.translation = [5.0, 1.0, 1.0]

        # when
        res = geoobject.contains_translation()

        # then
        self.assertTrue(res)
