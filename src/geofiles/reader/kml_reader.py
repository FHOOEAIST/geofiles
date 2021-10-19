from abc import ABC
import xml.etree.ElementTree as ET
from typing import List, Any, Dict

from geofiles.conversion.static import get_wgs_84
from geofiles.domain.face import Face
from geofiles.domain.geo_object import GeoObject
from geofiles.domain.geo_object_file import GeoObjectFile
from geofiles.reader.base import BaseReader
from geofiles.reader.xml_reader import XmlReader


class KmlReader(XmlReader, BaseReader, ABC):
    """
    Reader implementation for KML files
    Note: That only Solids containing Polygons are supported. Additionally, only the Exterior Linearrings are considered.
    """

    def __init__(self):
        """
        unique_vertices: defines that read vertices have to be unique
        """
        self.unique_vertices = False

    def _read_xml(self, xml: ET.Element) -> GeoObjectFile:
        result = GeoObjectFile()
        result.crs = get_wgs_84()

        self.remove_namespaces(xml)
        vertex_list: List[List[Any]] = []
        vertex_indices: Dict[str, int] = dict()
        placemarks = xml.findall(".//Placemark")
        for placemark in placemarks:
            geo_object = GeoObject()
            result.objects.append(geo_object)
            names = placemark.findall(".//name")
            if len(names) == 1:
                geo_object.name = names[0].text
            polygons = placemark.findall(".//Polygon")
            for polygon in polygons:
                coordinates = polygon.findall("./outerBoundaryIs/LinearRing/coordinates")
                if len(coordinates) == 1:
                    face_object = Face()
                    splitted_coordinates = coordinates[0].text.split("\n")
                    splitted_coordinates.pop()
                    for splitted_coordinate in [a for a in splitted_coordinates if a]:
                        splitted = [float(a) for a in splitted_coordinate.split(" ") if a]
                        self._filter_faces(self.unique_vertices, splitted, face_object, vertex_list, vertex_indices)
                    geo_object.faces.append(face_object)

        result.vertices = vertex_list
        return result
