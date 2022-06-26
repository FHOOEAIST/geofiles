import re
import xml.etree.ElementTree as ET
from abc import ABC
from typing import Any, Dict, List

from geofiles.conversion.static import triplewise
from geofiles.domain.face import Face
from geofiles.domain.geo_object import GeoObject
from geofiles.domain.geo_object_file import GeoObjectFile
from geofiles.reader.base import BaseReader
from geofiles.reader.xml_reader import XmlReader


class ColladaReader(XmlReader, BaseReader, ABC):
    """
    Reader implementation for collada (.dae) files
    """

    def __init__(self):
        """
        unique_vertices: defines that read vertices have to be unique
        """
        self.unique_vertices = False

    def read_xml(self, xml: ET.Element) -> GeoObjectFile:
        result = GeoObjectFile()
        self.remove_namespaces(xml)

        if xml.attrib.get("crs") is not None:
            result.crs = xml.attrib["crs"]

        geometries = xml.findall(".//library_geometries/geometry")
        vertex_list: List[List[Any]] = []
        vertex_indices: Dict[str, int] = dict()

        for geometry in geometries:
            geo_object = GeoObject()
            mesh = geometry.find("./mesh")
            if mesh is None:
                raise Exception("Could not find mesh element")
            triangles = mesh.find("./triangles")
            if triangles is None:
                raise Exception("Could not find triangles element")
            vertex_input = triangles.find("./input[@semantic='VERTEX']")
            if vertex_input is None:
                raise Exception(
                    "Could not find input element with semantic attribute VERTEX"
                )
            input_array_name = vertex_input.attrib["source"].replace("#", "")
            elem = mesh.find(f"./vertices[@id='{input_array_name}']")
            if elem is None:
                raise Exception("Could not find vertices element")
            input_elem = elem.find("./input")
            if input_elem is None:
                raise Exception("Could not find input element")
            input_array_name2 = input_elem.attrib["source"].replace("#", "")
            source = mesh.find(f"./source[@id='{input_array_name2}']")
            if source is None:
                raise Exception("Could not find source element")
            float_array = source.find("./float_array")
            if float_array is None:
                raise Exception("Could not find float_array element")
            params = source.findall("./technique_common/accessor/param")
            param_len = len(params)
            float_array_content = float_array.text
            if float_array_content is None:
                raise Exception("Could not find text of float_array element")
            positions = re.sub(
                r"\s+", " ", float_array_content.replace("\n", " ")
            ).split(" ")

            p_elem = triangles.find("./p")
            if p_elem is None:
                raise Exception("Could not find p_elem element")
            p_elem_content = p_elem.text
            if p_elem_content is None:
                raise Exception("Could not find text of p element")
            indices = re.sub(r"\s+", " ", p_elem_content.replace("\n", " ")).split(" ")
            for x in triplewise(indices):
                face = Face()
                for i in x:
                    p = []
                    for j in range(0, param_len):
                        p.append(float(positions[int(i) * 3 + j]))
                    self._filter_faces(
                        self.unique_vertices,
                        p,
                        face,
                        vertex_list,
                        vertex_indices,
                    )
                geo_object.faces.append(face)

            result.objects.append(geo_object)
        result.vertices = vertex_list
        return result
