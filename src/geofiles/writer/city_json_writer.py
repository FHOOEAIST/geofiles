import uuid
from abc import ABC
from typing import Any, Dict, List

from geofiles.domain.file_version import CityJsonVersion
from geofiles.domain.geo_object_file import GeoObjectFile
from geofiles.writer.base import BaseWriter
from geofiles.writer.json_writer import JsonWriter


class CityJsonWriter(JsonWriter, BaseWriter, ABC):
    """
    Writer implementation for creating GeoJSON geometry files
    """

    def __init__(self, version: CityJsonVersion = CityJsonVersion.V1_1):
        """
        :param version: The CityJSON version to be used
        """
        self.version = version

    def create_json(
        self,
        data: GeoObjectFile,
        random_seed: Any = None,
    ) -> Dict[Any, Any]:
        if data.is_origin_based():
            raise Exception("Geo-referenced data must not be origin based")

        if data.contains_rotation():
            raise Exception("CityJSON does not support rotational information")

        num_vertices = len(data.vertices)

        res: Dict[Any, Any] = dict()
        res["type"] = "CityJSON"

        if self.version == CityJsonVersion.V1_1:
            res["version"] = "1.1"
        else:
            res["version"] = "1.0"

        metadata: Dict[Any, Any] = dict()
        add_metadata = False
        if data.crs is not None:
            add_metadata = True
            metadata["referenceSystem"] = data.crs

        transform = dict()
        set_scale = False
        if data.contains_scaling():
            scale = data.scaling
            set_scale = True
        elif self.version != CityJsonVersion.V1_0:
            # scale is mandatory in CityJSON 1.1
            scale = [1, 1, 1]
            set_scale = True

        set_translate = False
        if data.contains_translation():
            translate = data.translation
            set_translate = True
        elif self.version != CityJsonVersion.V1_0:
            # translation is mandatory in CityJSON 1.1
            translate = [0, 0, 0]
            set_translate = True

        if set_scale:
            transform["scale"] = scale
        if set_translate:
            transform["translate"] = translate

        if len(transform) != 0:
            res["transform"] = transform

        if (
            data.min_extent is not None
            and data.max_extent is not None
            and len(data.min_extent) > 0
            and len(data.max_extent) > 0
        ):
            add_metadata = True
            metadata["geographicalExtent"] = data.min_extent + data.max_extent

        if add_metadata:
            res["metadata"] = metadata
        objects: Dict[Any, Any] = dict()
        res["CityObjects"] = objects
        for obj in data.objects:
            if (
                obj.contains_scaling()
                or obj.contains_rotation()
                or obj.contains_translation()
            ):
                raise Exception(
                    "CityJSON does not support local object transformation information"
                )
            cityobject: Dict[Any, Any] = dict()
            if obj.name == "" or obj.name is None:
                if random_seed is None:
                    objects[str(uuid.uuid4())] = cityobject
                else:
                    objects[str(uuid.UUID(int=random_seed, version=4))] = cityobject
            else:
                objects[obj.name] = cityobject
            cityobject["type"] = obj.get_meta_information_or_default(
                "type", "GenericCityObject"
            )
            geometries: List[Any] = []
            cityobject["geometry"] = geometries
            geometry: Dict[Any, Any] = dict()
            geometries.append(geometry)
            geometry["type"] = "MultiSurface"
            geometry["lod"] = 1
            boundaries: List[Any] = []
            geometry["boundaries"] = boundaries
            for face in obj.faces:
                boundary = []
                for idx in face.indices:
                    idx = int(idx)
                    if idx < 0:
                        boundary.append(num_vertices - idx)
                    else:
                        boundary.append(idx - 1)
                boundaries.append([boundary])
        res["vertices"] = data.vertices

        return res

    def get_file_type(self) -> str:
        """
        :return: the supported file type of this writer
        """
        return ".city.json"
