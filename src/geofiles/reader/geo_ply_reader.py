from abc import ABC
from typing import Iterable

from geofiles.domain.face import Face
from geofiles.domain.geo_object import GeoObject
from geofiles.domain.geo_object_file import GeoObjectFile
from geofiles.reader.base import BaseReader


class GeoPlyReader(BaseReader, ABC):
    """
    Reader implementaiton for geo-referenced .ply files (.geoply)
    """

    def _read(self, file: Iterable[str]) -> GeoObjectFile:
        res = GeoObjectFile()
        obj = GeoObject()
        res.objects.append(obj)
        num_of_vertices = 0
        search_for_vertices = False
        cnt = 0

        for line in file:
            trimmed = line.strip()
            if not trimmed:
                continue
            trimmed = " ".join(trimmed.split())
            if not search_for_vertices:
                if trimmed.startswith("crs"):
                    res.crs = trimmed[4:]
                elif trimmed.startswith("element vertex"):
                    num_of_vertices = int(trimmed[14:])
                elif trimmed.startswith("origin"):
                    res.origin = [float(a) for a in trimmed[7:].split(" ")]
                elif trimmed.startswith("scale"):
                    res.scaling = [float(a) for a in trimmed[6:].split(" ")]
                elif trimmed.startswith("translate"):
                    res.translation = [float(a) for a in trimmed[10:].split(" ")]
                elif trimmed.startswith("rotate"):
                    res.rotation = [float(a) for a in trimmed[7:].split(" ")]
                elif trimmed.startswith("extent"):
                    extent = [float(a) for a in trimmed[7:].split(" ")]
                    res.min_extent = extent[:3]
                    res.max_extent = extent[3:]
                elif trimmed.startswith("meta"):
                    splits = trimmed.split(" ")
                    if splits[0] == "meta":
                        target = obj.meta_information
                    else:
                        target = res.meta_information

                    if len(splits) > 3:
                        target[splits[1]] = tuple(splits[2:])
                    else:
                        target[splits[1]] = splits[2]
                elif trimmed.startswith("end_header"):
                    search_for_vertices = True
            else:
                splits = trimmed.split(" ")
                if cnt < num_of_vertices:
                    res.vertices.append([float(a) for a in splits])
                    cnt += 1
                else:
                    face = Face()
                    face.indices = [int(a) + 1 for a in splits[1:]]
                    obj.faces.append(face)

        return res
