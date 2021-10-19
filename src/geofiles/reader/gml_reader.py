from abc import ABC
import xml.etree.ElementTree as ET
from typing import List, Any, Dict

from geofiles.domain.face import Face
from geofiles.domain.geo_object import GeoObject
from geofiles.domain.geo_object_file import GeoObjectFile
from geofiles.reader.base import BaseReader
from geofiles.reader.xml_reader import XmlReader


class GmlReader(XmlReader, BaseReader, ABC):
    """
    Reader implementation for GML files
    Note: That only Solids containing Polygons are supported. Additionally, only the Exterior Linearrings are considered.
    """

    def __init__(self):
        """
        unique_vertices: defines that read vertices have to be unique
        """
        self.unique_vertices = False

    def _read_xml(self, xml: ET.Element) -> GeoObjectFile:
        result = GeoObjectFile()
        self.remove_namespaces(xml)

        solids = xml.findall(".//Solid")

        vertex_list: List[List[Any]] = []
        vertex_indices: Dict[str, int] = dict()

        if len(solids) > 0:
            first_solid = solids[0]
            result.crs = self._get_attribute(first_solid, "srsName")
            for solid in solids:
                if self._get_attribute(solid, "srsName") != result.crs:
                    raise Exception("Found non uniform CRS definition in Solid elements. Currently not supported in this implementation.")
                geo_object = GeoObject()

                polygons = solid.findall(".//Polygon")

                for polygon in polygons:
                    poslists = polygon.findall(".//exterior/LinearRing/posList")
                    face_object = Face()
                    for poslist in poslists:
                        splits = poslist.text.split(" ")
                        splits.pop()
                        for split in splits:
                            coordinate = [float(a) for a in split.split(",")]
                            self._filter_faces(self.unique_vertices, coordinate, face_object, vertex_list, vertex_indices)
                    geo_object.faces.append(face_object)
                result.objects.append(geo_object)

        result.vertices = vertex_list
        return result