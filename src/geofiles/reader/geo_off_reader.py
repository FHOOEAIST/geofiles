from abc import ABC

from geofiles.domain.geo_object_file import GeoObjectFile
from geofiles.domain.geo_object import GeoObject
from geofiles.domain.face import Face

from io import TextIOWrapper

from geofiles.reader.base import BaseReader


class GeoOffReader(BaseReader, ABC):
    """
    Reader implementaiton for geo-referenced .off files (.geooff)
    """
    def _read(self, file: TextIOWrapper) -> GeoObjectFile:
        res = GeoObjectFile()
        obj = GeoObject()
        res.objects.append(obj)
        next_line_crs = False
        next_line_definition = False
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

            if len(trimmed) == 0:
                continue

            if not search_for_vertices:
                if next_line_crs:
                    splits = trimmed.split(" ")
                    res.crs = splits[0]
                    if len(splits) > 1:
                        res.origin = splits[1:]
                    next_line_definition = True
                    next_line_crs = False
                elif next_line_definition:
                    split = trimmed.split(" ")
                    num_of_vertices = int(split[0])
                    next_line_definition = False
                    search_for_vertices = True
                elif trimmed.startswith("GeoOFF"):
                    next_line_crs = True
                elif trimmed.startswith("OFF"):
                    next_line_definition = True
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
