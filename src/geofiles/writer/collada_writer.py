import datetime
import uuid
import xml.etree.ElementTree as ET
from abc import ABC
from typing import Any, Optional

from geofiles.domain.geo_object_file import GeoObjectFile
from geofiles.writer.base import BaseWriter
from geofiles.writer.xml_writer import XmlWriter


class ColladaWriter(XmlWriter, BaseWriter, ABC):
    """
    Writer implementation for creating collada (.dae) geometry files
    """

    def __init__(self, date: Optional[datetime.datetime] = None):
        """
        :param date: Date used within the created/modified tags
        """
        self.date = date

    def create_xml(
        self, data: GeoObjectFile, random_seed: Any = None
    ) -> ET.ElementTree:
        self._contains_transformation_information(data)
        root = ET.Element("COLLADA")
        root.attrib["xmlns"] = "https://www.khronos.org/files/collada_schema_1_5"
        root.attrib["version"] = "1.5.0"
        if data.crs is not None:
            root.attrib["crs"] = data.crs

        asset = ET.Element("asset")
        root.append(asset)
        contributor = ET.Element("contributor")
        authoring_tool = ET.Element("authoring_tool")
        authoring_tool.text = "GeoFiles Project"
        contributor.append(authoring_tool)
        asset.append(contributor)
        created = ET.Element("created")

        if self.date is None:
            date = datetime.datetime.utcnow()
        else:
            date = self.date

        created.text = date.isoformat()
        asset.append(created)

        modified = ET.Element("modified")
        modified.text = date.isoformat()
        asset.append(modified)

        unit = ET.Element("unit")
        unit.attrib["meter"] = "1.000000"
        asset.append(unit)

        up_axis = ET.Element("up_axis")
        up_axis.text = "Y_UP"
        asset.append(up_axis)

        library_geometries = ET.Element("library_geometries")
        root.append(library_geometries)

        library_visual_scenes = ET.Element("library_visual_scenes")
        root.append(library_visual_scenes)
        visual_scene = ET.Element("visual_scene")
        visual_scene.attrib["id"] = "scene"
        library_visual_scenes.append(visual_scene)

        scene = ET.Element("scene")
        root.append(scene)
        instance_visual_scene = ET.Element("instance_visual_scene")
        scene.append(instance_visual_scene)
        instance_visual_scene.attrib["url"] = "#scene"

        float_array_cnt = 0
        for geoobj in data.objects:
            geometry = ET.Element("geometry")
            library_geometries.append(geometry)

            if geoobj.name is not None:
                name = geoobj.name
                geometry.attrib["id"] = name
                geometry.attrib["name"] = name
            else:
                if random_seed is None:
                    obj_id = str(uuid.uuid4())
                else:
                    obj_id = str(uuid.UUID(int=random_seed, version=4))
                geometry.attrib["id"] = obj_id
                geometry.attrib["name"] = obj_id
                name = obj_id

            node = ET.Element("node")
            visual_scene.append(node)
            node.attrib["id"] = name
            node.attrib["name"] = name
            instance_geometry = ET.Element("instance_geometry")
            instance_geometry.attrib["url"] = f"#{name}"
            node.append(instance_geometry)

            mesh = ET.Element("mesh")
            geometry.append(mesh)

            source = ET.Element("source")
            mesh.append(source)
            source_name = f"{name}-vertices"
            source.attrib["id"] = source_name

            float_array = ET.Element("float_array")
            source.append(float_array)
            float_array_id = f"ID-array-{float_array_cnt}"
            float_array_cnt += 1
            float_array.attrib["id"] = float_array_id
            flat_list = [str(x) for xs in data.vertices for x in xs]
            listlen = len(flat_list)
            float_array.attrib["count"] = str(listlen)
            float_array.text = " ".join(flat_list)

            technique_common = ET.Element("technique_common")
            source.append(technique_common)

            accessor = ET.Element("accessor")
            accessor.attrib["source"] = f"#{float_array_id}"
            accessor.attrib["count"] = str(int(listlen / 3))
            accessor.attrib["stride"] = "3"
            technique_common.append(accessor)

            param1 = ET.Element("param")
            param1.attrib["name"] = "X"
            param1.attrib["type"] = "float"
            param2 = ET.Element("param")
            param2.attrib["name"] = "Y"
            param2.attrib["type"] = "float"
            param3 = ET.Element("param")
            param3.attrib["name"] = "Z"
            param3.attrib["type"] = "float"
            accessor.append(param1)
            accessor.append(param2)
            accessor.append(param3)

            vertices = ET.Element("vertices")
            vertices_id = f"{name}-vertices"
            vertices.attrib["id"] = vertices_id
            mesh.append(vertices)
            vertices_input = ET.Element("input")
            vertices.append(vertices_input)
            vertices_input.attrib["semantic"] = "POSITION"
            vertices_input.attrib["source"] = f"#{source_name}"

            triangles = ET.Element("triangles")
            triangles.attrib["count"] = str(len(geoobj.faces))
            mesh.append(triangles)
            triangles_input = ET.Element("input")
            triangles.append(triangles_input)
            triangles_input.attrib["semantic"] = "VERTEX"
            triangles_input.attrib["offset"] = "0"
            triangles_input.attrib["source"] = f"#{vertices_id}"

            p = ET.Element("p")
            triangles.append(p)
            face_indices = []
            for face in geoobj.faces:
                for idx in face.indices:
                    face_indices.append(str(idx - 1))
            p.text = " ".join(face_indices)

        return ET.ElementTree(root)

    def get_file_type(self) -> str:
        """
        :return: the supported file type of this writer
        """
        return ".dae"
