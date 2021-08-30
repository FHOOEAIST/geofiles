import uuid
from abc import ABC
from io import TextIOWrapper

from geofiles.conversion.static import get_wgs_84
from geofiles.domain.geo_object import GeoObject
from geofiles.domain.geo_object_file import GeoObjectFile
from geofiles.writer.base import BaseWriter
import xml.etree.ElementTree as ET


class GmlWriter(BaseWriter, ABC):
    """
    Writer implementation for creating GML geometry files
    """

    def _write(self, file: TextIOWrapper, data: GeoObjectFile,  write_binary: bool, random_seed):
        """
        Write implementation
        :param file: target to be written
        :param data: content to be written
        :param write_binary: flag if file is a binary file
        :return:
        """
        self._contains_transformation_information(data)

        if "b" not in file.mode.lower():
            raise Exception("File must be opened in binary mode for GML")

        if data.crs is None:
            raise Exception("File must be geo-referenced")

        if data.is_origin_based():
            raise Exception("Geo-referenced data must not be origin based")

        attributes = dict()
        attributes["xmlns:gml"] = "http://www.opengis.net/gml/3.2"
        root = ET.Element('root', attributes)
        for obj in data.objects:
            obj: GeoObject = obj
            solid = ET.Element("gml:Solid")
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
                    id = str(uuid.uuid4())
                else:
                    id = str(uuid.UUID(int=random_seed, version=4))
                polygon.attrib["gml:id"] = id
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

        tree = ET.ElementTree(root)
        tree.write(file, encoding='ascii', xml_declaration=True)

    def get_file_type(self) -> str:
        """
        :return: the supported file type of this writer
        """
        return ".gml"
