import json
import uuid
from abc import ABC
from io import TextIOWrapper
from typing import Any, Dict, List

from geofiles.domain.geo_object_file import GeoObjectFile
from geofiles.writer.base import BaseWriter


class CityJsonWriter(BaseWriter, ABC):
    """
    Writer implementation for creating GeoJSON geometry files
    """

    def _write(
        self,
        file: TextIOWrapper,
        data: GeoObjectFile,
        write_binary: bool,
        random_seed: Any,
    ) -> None:
        if data.is_origin_based():
            raise Exception("Geo-referenced data must not be origin based")

        self._contains_transformation_information(data)

        num_vertices = len(data.vertices)

        res: Dict[Any, Any] = dict()
        res["type"] = "CityJSON"
        res["version"] = "1.0"
        metadata: Dict[Any, Any] = dict()
        add_metadata = False
        if data.crs is not None:
            add_metadata = True
            metadata["referenceSystem"] = data.crs

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
            cityobject: Dict[Any, Any] = dict()
            if obj.name == "" or obj.name is None:
                if random_seed is None:
                    objects[str(uuid.uuid4())] = cityobject
                else:
                    objects[str(uuid.UUID(int=random_seed, version=4))] = cityobject
            else:
                objects[obj.name] = cityobject
            cityobject["type"] = "GenericCityObject"
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

        json.dump(res, file)

    def get_file_type(self) -> str:
        """
        :return: the supported file type of this writer
        """
        return ".city.json"
