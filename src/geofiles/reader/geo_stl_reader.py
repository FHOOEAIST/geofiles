from abc import ABC
from io import TextIOWrapper
from typing import Any, Dict

from geofiles.domain.face import Face
from geofiles.domain.geo_object import GeoObject
from geofiles.domain.geo_object_file import GeoObjectFile
from geofiles.reader.base import BaseReader


class GeoStlReader(BaseReader, ABC):
    """
    Reader implementaiton for geo-referenced .stl files (.geostl)
    """

    def _read(self, file: TextIOWrapper) -> GeoObjectFile:

        res = GeoObjectFile()
        obj = GeoObject()
        res.objects.append(obj)
        vertices: Dict[Any, Any] = dict()
        cnt = 1
        current_face: Face
        while True:
            # Get next line from file
            line = file.readline()

            # if line is empty
            # end of file is reached
            if not line:
                break
            trimmed = line.strip()
            trimmed = " ".join(trimmed.split())

            if trimmed.startswith("geosolid") or trimmed.startswith("solid"):
                splits = trimmed.split(" ")
                res.crs = splits[1]
                list_len = len(splits)
                if list_len in (5, 6):
                    res.origin = [float(a) for a in splits[2:5]]
                    if list_len == 6:
                        obj.name = splits[-1]
                elif list_len == 2:
                    obj.name = splits[-1]
            elif trimmed.startswith("facet"):
                current_face = Face()
                obj.faces.append(current_face)
            elif trimmed.startswith("vertex"):
                v = trimmed[7:]
                idx = vertices.get(v)
                if idx is None:
                    vertices[v] = cnt
                    idx = cnt
                    cnt += 1
                current_face.indices.append(idx)

        for vs in vertices:
            splits = vs.split(" ")
            x = float(splits[0])
            y = float(splits[1])
            z = float(splits[2])
            res.vertices.append([x, y, z])

        return res
