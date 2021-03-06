import xml.etree.ElementTree as ET
from abc import ABC
from typing import Any

from geofiles.conversion.static import get_wgs_84
from geofiles.domain.geo_object_file import GeoObjectFile
from geofiles.writer.base import BaseWriter
from geofiles.writer.xml_writer import XmlWriter


class KmlWriter(XmlWriter, BaseWriter, ABC):
    """
    Writer implementation for creating KML geometry files
    """

    def create_xml(
        self, data: GeoObjectFile, random_seed: Any = None
    ) -> ET.ElementTree:
        self._contains_transformation_information(data)

        if data.crs != get_wgs_84():
            raise Exception("Kml requires WGS:84 coordinate system")

        if data.is_origin_based():
            raise Exception("Geo-referenced data must not be origin based")

        root = ET.Element("kml")
        root.attrib["xmlns"] = "http://www.opengis.net/kml/2.2"
        for obj in data.objects:
            if (
                obj.contains_scaling()
                or obj.contains_rotation()
                or obj.contains_translation()
            ):
                raise Exception(
                    "KML does not support local object transformation information"
                )
            placemark = ET.Element(
                obj.get_meta_information_or_default("type", "Placemark")
            )
            root.append(placemark)
            name = ET.Element("name")
            name.text = obj.name
            placemark.append(name)
            for face in obj.faces:
                polygon = ET.Element("Polygon")
                placemark.append(polygon)
                extrude = ET.Element("extrude")
                extrude.text = "0"
                polygon.append(extrude)
                altitude_mode = ET.Element("altitudeMode")
                altitude_mode.text = "absolute"
                polygon.append(altitude_mode)
                outer_boundary = ET.Element("outerBoundaryIs")
                polygon.append(outer_boundary)
                linear_ring = ET.Element("LinearRing")
                outer_boundary.append(linear_ring)
                coordinates = ET.Element("coordinates")
                coordinates.text = "\n"
                linear_ring.append(coordinates)
                for idx in face.indices:
                    coords = data.get_vertex(idx)
                    for coord in coords:
                        coordinates.text += str(coord) + " "
                    coordinates.text += "\n"

                coords = data.get_vertex(face.indices[0])
                for coord in coords:
                    coordinates.text += str(coord) + " "

        return ET.ElementTree(root)

    def get_file_type(self) -> str:
        """
        :return: the supported file type of this writer
        """
        return ".kml"
