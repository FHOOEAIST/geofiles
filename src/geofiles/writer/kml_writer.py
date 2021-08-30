import xml.etree.ElementTree as ET
from abc import ABC
from io import TextIOWrapper

from geofiles.conversion.static import get_wgs_84
from geofiles.domain.geo_object import GeoObject
from geofiles.domain.geo_object_file import GeoObjectFile
from geofiles.writer.base import BaseWriter


class KmlWriter(BaseWriter, ABC):
    """
    Writer implementation for creating KML geometry files
    """

    def _write(
        self, file: TextIOWrapper, data: GeoObjectFile, write_binary: bool, random_seed
    ):
        """
        Write implementation
        :param file: target to be written
        :param data: content to be written
        :param write_binary: flag if file is a binary file
        :return:
        """
        self._contains_transformation_information(data)

        if "b" not in file.mode.lower():
            raise Exception("File must be opened in binary mode for KML")

        if data.crs != get_wgs_84():
            raise Exception("Kml requires WGS:84 coordinate system")

        if data.is_origin_based():
            raise Exception("Geo-referenced data must not be origin based")

        root = ET.Element("kml")
        root.attrib["xmlns"] = "http://www.opengis.net/kml/2.2"
        for obj in data.objects:
            obj: GeoObject = obj
            placemark = ET.Element("Placemark")
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

        tree = ET.ElementTree(root)
        tree.write(file, encoding="ascii", xml_declaration=True)

    def get_file_type(self) -> str:
        """
        :return: the supported file type of this writer
        """
        return ".kml"
