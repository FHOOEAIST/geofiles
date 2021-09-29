import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod
from io import TextIOWrapper
from typing import Any

from geofiles.domain.geo_object_file import GeoObjectFile
from geofiles.writer.base import BaseWriter


class XmlWriter(BaseWriter, ABC):
    """
    Basic writer implementations for xml based file formats
    """

    @abstractmethod
    def create_xml(self, data: GeoObjectFile, random_seed: Any) -> ET.ElementTree:
        """
        Creates a json representation of the given GeoObjectFile
        """
        return ET.ElementTree()

    def write_to_string(
        self, data: GeoObjectFile, write_binary: bool = False, random_seed: Any = None
    ) -> str:
        et = self.create_xml(data, random_seed)
        encoding = "ascii" if write_binary else "utf8"
        return str(
            ET.tostring(et.getroot(), encoding=encoding, method="xml").decode(encoding)
        )

    def _write(
        self,
        file: TextIOWrapper,
        data: GeoObjectFile,
        write_binary: bool,
        random_seed: Any,
    ) -> None:
        if "b" not in file.mode.lower():
            raise Exception("File must be opened in binary mode")
        et = self.create_xml(data, random_seed)
        et.write(file, encoding="ascii", xml_declaration=True)
