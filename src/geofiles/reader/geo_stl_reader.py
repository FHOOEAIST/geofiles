from abc import ABC

from geofiles.domain.geo_object_file import GeoObjectFile
from geofiles.domain.geo_object import GeoObject
from geofiles.domain.face import Face

from io import TextIOWrapper

from geofiles.reader.base import BaseReader


class GeoStlReader(BaseReader, ABC):
    """
    Reader implementaiton for geo-referenced .stl files (.geostl)
    """
    def _read(self, file: TextIOWrapper) -> GeoObjectFile:

        res = GeoObjectFile()
        obj = GeoObject()
        res.objects.append(obj)
        vertices = dict()
        cnt = 1
        current_face = None
        while True:
            # Get next line from file
            line = file.readline()

            # if line is empty
            # end of file is reached
            if not line:
                break
            trimmed = line.strip()
            trimmed = ' '.join(trimmed.split())

            if trimmed.startswith("geosolid") or trimmed.startswith("solid"):
                splits = trimmed.split(" ")
                res.crs = splits[1]
                if len(splits) > 3:
                    res.origin = splits[2:4]
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

        for vs in vertices.keys():
            splits = vs.split(" ")
            x = float(splits[0])
            y = float(splits[1])
            z = float(splits[2])
            res.vertices.append([x, y, z])

        return res

