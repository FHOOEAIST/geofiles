# pylint: disable=R0201
import xml.etree.ElementTree as ET
from abc import ABC
from typing import Any, Dict, List

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

    def __init__(self) -> None:
        """
        unique_vertices: defines that read vertices have to be unique
        """
        self.unique_vertices = False

    def read_xml(self, xml: ET.Element) -> GeoObjectFile:
        result = GeoObjectFile()
        self.remove_namespaces(xml)
        self._internal_read_xml(result, xml, ".//Solid")
        return result

    def _internal_decorate_object(self, _: ET.Element, __: GeoObject) -> None:
        """
        Internal method for decorating the current GeoObject
        :param _: current xml object
        :param __: current geo object
        """
        return None

    def _internal_read_xml(
        self, result: GeoObjectFile, xml: ET.Element, baseelements: str
    ) -> None:
        """
        Internal method for reading a gml xml file
        :param result: The resulting GeoObjectfiled
        :param xml: root element
        :param baseelements: xpath string defining the base elements
        """
        solids = xml.findall(baseelements)

        vertex_list: List[List[Any]] = []
        if len(result.vertices) != 0:
            vertex_list = result.vertices.copy()
        vertex_indices: Dict[str, int] = dict()

        if len(solids) > 0:
            first_solid = solids[0]
            crs = self._get_attribute(first_solid, "srsName")
            if crs is not None:
                result.crs = crs
            for solid in solids:
                solid_crs = self._get_attribute(solid, "srsName")
                if solid_crs is not None and solid_crs != result.crs:
                    raise Exception(
                        "Found non uniform CRS definition in Solid elements. Currently not supported in this implementation."
                    )
                geo_object = GeoObject()
                self._internal_decorate_object(solid, geo_object)
                polygons = solid.findall(".//Polygon")

                for polygon in polygons:
                    linearrings = polygon.findall(".//exterior/LinearRing")
                    for linearring in linearrings:
                        face_object = Face()
                        poslists = linearring.findall("./posList")
                        for poslist in poslists:
                            if poslist is not None and poslist.text is not None:
                                splits = poslist.text.split(" ")
                                splits.pop()
                                for split in splits:
                                    coordinate = [float(a) for a in split.split(",")]
                                    self._filter_faces(
                                        self.unique_vertices,
                                        coordinate,
                                        face_object,
                                        vertex_list,
                                        vertex_indices,
                                    )

                        positions = linearring.findall("./pos")
                        for position in positions:
                            if position is not None and position.text is not None:
                                splits = position.text.split(" ")
                                coordinate = [float(a) for a in splits]
                                self._filter_faces(
                                    self.unique_vertices,
                                    coordinate,
                                    face_object,
                                    vertex_list,
                                    vertex_indices,
                                )
                        geo_object.faces.append(face_object)
                result.objects.append(geo_object)

        result.vertices = vertex_list
