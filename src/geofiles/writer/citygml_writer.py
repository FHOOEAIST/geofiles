import uuid
import xml.etree.ElementTree as ET
from abc import ABC
from typing import Any, Dict, List

from geofiles.domain.geo_object import GeoObject
from geofiles.domain.geo_object_file import GeoObjectFile
from geofiles.writer.base import BaseWriter
from geofiles.writer.xml_writer import XmlWriter


class CityGmlWriter(XmlWriter, BaseWriter, ABC):
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
        attributes["xmlns:gml"] = "http://www.opengis.net/gml/"
        attributes["xmlns"] = "http://www.opengis.net/citygml/profiles/base/1.0"
        attributes["xmlns:core"] = "http://www.opengis.net/citygml/1.0"
        attributes["xmlns:bldg"] = "http://www.opengis.net/citygml/building/1.0"
        attributes["xmlns:grp"] = "http://www.opengis.net/citygml/cityobjectgroup/1.0"
        attributes["xmlns:app"] = "http://www.opengis.net/citygml/appearance/1.0"
        attributes["xmlns:gml"] = "http://www.opengis.net/gml"
        attributes["xmlns:xAL"] = "urn:oasis:names:tc:ciq:xsdschema:xAL:2.0"
        attributes["xmlns:xlink"] = "http://www.w3.org/1999/xlink"
        attributes["xmlns:xsi"] = "http://www.w3.org/2001/XMLSchema-instance"
        attributes["xmlns:frn"] = "http://www.opengis.net/citygml/cityfurniture/1.0"
        attributes["xmlns:wtr"] = "http://www.opengis.net/citygml/waterbody/1.0"
        attributes["xmlns:dem"] = "http://www.opengis.net/citygml/relief/1.0"
        attributes["xmlns:luse"] = "http://www.opengis.net/citygml/landuse/1.0"
        attributes["xmlns:veg"] = "http://www.opengis.net/citygml/vegetation/1.0"
        attributes["xmlns:tran"] = "http://www.opengis.net/citygml/transportation/1.0"
        attributes["xmlns:gen"] = "http://www.opengis.net/citygml/generics/1.0"
        attributes[
            "xsi:schemaLocation"
        ] = "http://www.opengis.net/citygml/1.0 http://schemas.opengis.net/citygml/1.0/cityGMLBase.xsd http://www.opengis.net/citygml/appearance/1.0 http://schemas.opengis.net/citygml/appearance/1.0/appearance.xsd http://www.opengis.net/citygml/building/1.0 http://schemas.opengis.net/citygml/building/1.0/building.xsd http://www.opengis.net/citygml/cityfurniture/1.0 http://schemas.opengis.net/citygml/cityfurniture/1.0/cityFurniture.xsd http://www.opengis.net/citygml/vegetation/1.0 http://schemas.opengis.net/citygml/vegetation/1.0/vegetation.xsd http://www.opengis.net/citygml/generics/1.0 http://schemas.opengis.net/citygml/generics/1.0/generics.xsd http://www.opengis.net/citygml/transportation/1.0 http://schemas.opengis.net/citygml/transportation/1.0/transportation.xsd http://www.opengis.net/citygml/waterbody/1.0 http://schemas.opengis.net/citygml/waterbody/1.0/waterBody.xsd http://www.opengis.net/citygml/landuse/1.0 http://schemas.opengis.net/citygml/landuse/1.0/landUse.xsd http://www.opengis.net/citygml/relief/1.0 http://schemas.opengis.net/citygml/relief/1.0/relief.xsd"
        root = ET.Element("core:CityModel", attributes)
        bounded_by = ET.Element("gml:boundedBy")
        root.append(bounded_by)
        envelope = ET.Element("gml:Envelope")
        envelope.attrib["srsName"] = data.crs
        envelope.attrib["srsDimension"] = "3"
        bounded_by.append(envelope)
        if (
            data.contains_extent()
            and data.min_extent is not None
            and data.max_extent is not None
        ):
            lower_corner = ET.Element("gml:lowerCorner")
            lower_corner.text = " ".join([str(x) for x in data.min_extent])
            envelope.append(lower_corner)
            upper_corner = ET.Element("gml:upperCorner")
            upper_corner.text = " ".join([str(x) for x in data.max_extent])
            envelope.append(upper_corner)

        buildings: Dict[str, List[GeoObject]] = dict()
        supported_types = [
            "Building",
            "CeilingSurface",
            "InteriorWallSurface",
            "FloorSurface",
            "RoofSurface",
            "WallSurface",
            "GroundSurface",
            "ClosureSurface",
            "BuildingInstallation",
        ]
        for obj in data.objects:
            obj_type = obj.get_meta_information_or_default("type", None)
            if obj_type in ["SolitaryVegetationObject", "CityFurniture", "LandUse"]:
                continue
            if obj_type is not None and obj_type not in supported_types:
                raise Exception(
                    f"Type ({obj_type}) not supported. Only CityGML types supported: {' '.join(supported_types)}"
                )

            if random_seed is None:
                obj_id = str(uuid.uuid4())
            else:
                obj_id = str(uuid.UUID(int=random_seed, version=4))

            if obj_type == "Building" or obj_type is None:
                building_id = obj.get_meta_information_or_default("id", obj_id)
                if buildings.get(building_id) is None:
                    buildings[building_id] = []
                if obj_type is None:
                    obj.set_type("GenericCityObject")
                    buildings[building_id] = [obj]
            elif obj.parent is not None:
                parent_id = obj.parent.get_meta_information_or_default("id", obj_id)
                if buildings.get(parent_id) is None:
                    buildings[parent_id] = []
                buildings[parent_id].append(obj)

        for k, v in buildings.items():
            com = ET.Element("core:cityObjectMember")
            root.append(com)
            building = ET.Element("bldg:Building")
            building.attrib["gml:id"] = k
            com.append(building)
            for obj in v:
                bounded_by = ET.Element("bldg:boundedBy")
                building.append(bounded_by)
                surface = ET.Element(f"bldg:{obj.get_type()}")
                bounded_by.append(surface)
                lod3_multi_surface = ET.Element("bldg:lod3MultiSurface")
                surface.append(lod3_multi_surface)
                multi_surface = ET.Element("gml:MultiSurface")
                lod3_multi_surface.append(multi_surface)
                surface_member = ET.Element("gml:surfaceMember")
                multi_surface.append(surface_member)
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
        return ".citygml"
