from abc import ABC

from geofiles.domain.geo_object_file import GeoObjectFile
from geofiles.domain.geo_object import GeoObject
from geofiles.domain.face import Face

from io import TextIOWrapper

from geofiles.reader.base import BaseReader


class GeoPlyReader(BaseReader, ABC):
    """
    Reader implementaiton for geo-referenced .ply files (.geoply)
    """
    def _read(self, file: TextIOWrapper) -> GeoObjectFile:
        res = GeoObjectFile()
        obj = GeoObject()
        res.objects.append(obj)
        num_of_vertices = 0
        search_for_vertices = False
        cnt = 0
        while True:
            # Get next line from file
            line = file.readline()

            # if line is empty
            # end of file is reached
            if not line:
                break
            trimmed = line.strip()
            trimmed = ' '.join(trimmed.split())
            if not search_for_vertices:
                if trimmed.startswith("crs"):
                    res.crs = trimmed[4:]
                elif trimmed.startswith("element vertex"):
                    num_of_vertices = int(trimmed[14:])
                elif trimmed.startswith("origin"):
                    res.origin = trimmed[7:].split(" ")
                elif trimmed.startswith("scale"):
                    res.scaling = trimmed[6:].split(" ")
                elif trimmed.startswith("translate"):
                    res.translation = trimmed[10:].split(" ")
                elif trimmed.startswith("rotate"):
                    res.rotation = trimmed[7:].split(" ")
                elif trimmed.startswith("end_header"):
                    search_for_vertices = True
            else:
                splits = trimmed.split(" ")
                if cnt < num_of_vertices:
                    res.vertices.append(splits)
                    cnt += 1
                else:
                    face = Face()
                    face.indices = [int(a) + 1 for a in splits[1:]]
                    obj.faces.append(face)

        return res