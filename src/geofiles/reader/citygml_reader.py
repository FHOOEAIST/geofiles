import uuid
import xml.etree.ElementTree as ET
from abc import ABC

from geofiles.domain.geo_object import GeoObject
from geofiles.domain.geo_object_file import GeoObjectFile
from geofiles.reader.base import BaseReader
from geofiles.reader.gml_reader import GmlReader
from geofiles.reader.xml_reader import XmlReader


class CityGmlReader(GmlReader, XmlReader, BaseReader, ABC):
    """
    Reader implementation for City GML files
    Note: Only polygons with their Exterior Linearrings are considered
    """

    def __init__(self):
        super().__init__()
        self.curr_object = None
        self.curr_object_used = False

    def read_xml(self, xml: ET.Element) -> GeoObjectFile:
        result = GeoObjectFile()
        self.remove_namespaces(xml)
        envelopes = xml.findall("./boundedBy/Envelope")
        for envelope in envelopes:
            crs = envelope.attrib.get("srsName")
            if crs is not None:
                result.crs = crs
                break

        city_objects = xml.findall(".//cityObjectMember/Building")

        for city_object in city_objects:
            self.curr_object = GeoObject()
            self.curr_object.set_type("Building")
            city_object_id = city_object.attrib.get("id")
            if city_object_id is None:
                city_object_id = str(uuid.uuid4())
            self.curr_object.meta_information["id"] = city_object_id
            for surface_class in [
                "GenericCityObject",
                "CeilingSurface",
                "InteriorWallSurface",
                "FloorSurface",
                "RoofSurface",
                "WallSurface",
                "GroundSurface",
                "ClosureSurface",
                "BuildingInstallation",
            ]:
                self._internal_read_xml(result, city_object, f".//{surface_class}")
            if self.curr_object_used:
                result.objects.append(self.curr_object)
                self.curr_object_used = False
        self.curr_object = None
        return result

    def _internal_decorate_object(
        self, xml_object: ET.Element, geo_object: GeoObject
    ) -> None:
        """
        Internal method for decorating the current GeoObject
        :param xml_object: current xml object
        :param geo_object: current geo object
        """
        geo_object.parent = self.curr_object
        geo_object.set_type(xml_object.tag)
        self.curr_object_used = True
