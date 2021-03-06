import uuid
import xml.etree.ElementTree as ET
from abc import ABC
from typing import Any

from geofiles.domain.geo_object_file import GeoObjectFile
from geofiles.writer.base import BaseWriter
from geofiles.writer.xml_writer import XmlWriter


class GmlWriter(XmlWriter, BaseWriter, ABC):
    """
    Writer implementation for creating GML geometry files
    """

    def create_xml(
        self, data: GeoObjectFile, random_seed: Any = None
    ) -> ET.ElementTree:
        if data.is_origin_based():
            raise Exception("Geo-referenced data must not be origin based")

        self._contains_transformation_information(data)

        if data.crs is None:
            raise Exception("File must be geo-referenced")

        if data.is_origin_based():
            raise Exception("Geo-referenced data must not be origin based")

        attributes = dict()
        attributes["xmlns:gml"] = "http://www.opengis.net/gml/3.2"
        root = ET.Element("root", attributes)
        for obj in data.objects:
            if (
                obj.contains_scaling()
                or obj.contains_rotation()
                or obj.contains_translation()
            ):
                raise Exception(
                    "GML does not support local object transformation information"
                )
            solid = ET.Element(obj.get_meta_information_or_default("type", "gml:Solid"))
            solid.attrib = dict()
            solid.attrib["srsName"] = data.crs
            solid.attrib["srsDimension"] = "3"
            root.append(solid)

            exterior = ET.Element("gml:exterior")
            solid.append(exterior)
            composite_surface = ET.Element("gml:CompositeSurface")
            exterior.append(composite_surface)
            surface_member = ET.Element("gml:surfaceMember")
            composite_surface.append(surface_member)
            for face in obj.faces:
                polygon = ET.Element("gml:Polygon")
                polygon.attrib = dict()
                if random_seed is None:
                    polygon_id = str(uuid.uuid4())
                else:
                    polygon_id = str(uuid.UUID(int=random_seed, version=4))
                polygon.attrib["gml:id"] = polygon_id
                surface_member.append(polygon)
                boundaries = ET.Element("gml:exterior")
                polygon.append(boundaries)
                linearring = ET.Element("gml:LinearRing")
                boundaries.append(linearring)
                coordinates = ET.Element("gml:posList")
                linearring.append(coordinates)
                coordinates.text = ""
                for idx in face.indices:
                    vertex = [str(a) for a in data.get_vertex(idx)]
                    coordinates.text += ",".join(vertex)
                    coordinates.text += " "

                vertex = [str(a) for a in data.get_vertex(face.indices[0])]
                coordinates.text += ",".join(vertex)

        return ET.ElementTree(root)

    def get_file_type(self) -> str:
        """
        :return: the supported file type of this writer
        """
        return ".gml"
