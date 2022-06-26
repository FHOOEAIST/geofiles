import re
import xml.etree.ElementTree as ET
from abc import ABC
from typing import List, Any, Dict

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
            geoObject = GeoObject()
            mesh = geometry.find("./mesh")
            triangles = mesh.find("./triangles")
            input_array_name = triangles.find("./input[@semantic='VERTEX']").attrib["source"].replace("#", "")
            elem = mesh.find(f"./vertices[@id='{input_array_name}']")

            input_array_name2 = elem.find("./input").attrib["source"].replace("#", "")
            source = mesh.find(f"./source[@id='{input_array_name2}']")
            float_array = source.find(f"./float_array")
            params = source.find("./technique_common/accessor")
            param_len = len(params)
            positions = re.sub('\s+', ' ', float_array.text.replace("\n", " ")).split(" ")
            indices = re.sub('\s+', ' ', triangles.find("./p").text.replace("\n", " ")).split(" ")
            for x in self.tripplewise(indices):
                face = Face()
                for i in x:
                    p = []
                    for j in range(0, param_len):
                        p.append(float(positions[int(i)*3+j]))
                    self._filter_faces(
                        self.unique_vertices,
                        p,
                        face,
                        vertex_list,
                        vertex_indices,
                    )
                geoObject.faces.append(face)

            result.objects.append(geoObject)
        result.vertices = vertex_list
        return result

    def tripplewise(self, iterable):
        """
        Method for accessing a tripple from a list
        """
        a = iter(iterable)
        return zip(a, a, a)
