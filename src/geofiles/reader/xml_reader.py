import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod
from typing import Iterable, Optional

from geofiles.domain.geo_object_file import GeoObjectFile
from geofiles.reader.base import BaseReader


class XmlReader(BaseReader, ABC):
    """
    Base class for reading xml-based files
    """

    def _read(self, file: Iterable[str]) -> GeoObjectFile:
        xml_file = "".join(file)
        tree = ET.fromstring(xml_file)

        return self.read_xml(tree)

    @abstractmethod
    def read_xml(self, xml: ET.Element) -> GeoObjectFile:
        """
        Read implementation for xml based files
        :param xml: parsed element tree representation
        :return: Domain representation of the GeoObjectFile
        """
        return GeoObjectFile()

    def remove_namespaces(self, el: ET.Element) -> None:
        """
        Recursively search this element tree, removing namespaces.
        Source: https://stackoverflow.com/a/32552776
        :param el: Element for which namespace should be removed
        :return: None
        """
        if el.tag.startswith("{"):
            el.tag = el.tag.split("}", 1)[1]  # strip namespace
        for k in el.attrib.keys():
            if k.startswith("{"):
                k2 = k.split("}", 1)[1]
                el.attrib[k2] = el.attrib[k]
                del el.attrib[k]
        for child in el:
            self.remove_namespaces(child)

    @staticmethod
    def _get_attribute(xml: ET.Element, attribute_name: str) -> Optional[str]:
        """
        Get an attribute by name ignoring the namespace
        :param xml: element containing the attribute
        :param attribute_name: Name of the searched attribute
        :return: The value of the attribute if available, else None
        """
        for key, value in xml.attrib.items():
            if key.endswith(attribute_name):
                return value

        return None
