from abc import ABC
from typing import Any, Iterable

from geofiles.domain.face import Face
from geofiles.domain.geo_object import GeoObject
from geofiles.domain.geo_object_file import GeoObjectFile
from geofiles.reader.base import BaseReader


class GeoOffReader(BaseReader, ABC):
    """
    Reader implementaiton for geo-referenced .off files (.geooff)
    """

    def _read(self, file: Iterable[str]) -> GeoObjectFile:
        res = GeoObjectFile()
        obj = GeoObject()
        res.objects.append(obj)
        num_of_vertices = 0
        search_for_vertices = False
        cnt = 0

        headerdefinition = []
        found_headerdefinition = False

        for line in file:
            trimmed = line.strip()
            if not trimmed:
                continue
            trimmed = " ".join(trimmed.split())

            if not found_headerdefinition:
                # We have not found a header definition yet, so search for a GeoOFF or OFF header
                idx = trimmed.find("GeoOFF")
                if idx >= 0:
                    # found a GeoOFF header, so will look for the crs definition + further options
                    headerdefinition.append("crs")
                    postfix = trimmed[idx + len("GeoOFF") :]
                    found_headerdefinition = True
                    for e in postfix:
                        headerdefinition.append(e)
                    headerdefinition.append("header")
                elif trimmed.endswith("OFF"):
                    # found a classic OFF file
                    found_headerdefinition = True
                    headerdefinition.append("header")
            elif search_for_vertices:
                # We already looking for vertices and faces, since we know the number of vertices, just count to know when the faces start
                splits = trimmed.split(" ")
                if cnt < num_of_vertices:
                    coordinates = [float(a) for a in splits]
                    res.vertices.append(
                        coordinates[:3]
                    )  # we are only interested in the coordinates and not in optional additional information
                    cnt += 1
                else:
                    face = Face()
                    face.indices = [int(a) + 1 for a in splits[1:]]
                    obj.faces.append(face)
            elif found_headerdefinition:
                element = headerdefinition.pop(0)
                splits = trimmed.split(" ")

                if element == "crs":
                    res.crs = splits[0]
                elif element == "header":
                    num_of_vertices = int(splits[0])
                    search_for_vertices = True
                elif element == "o":
                    res.origin = [float(a) for a in splits]
                elif element == "e":
                    extents = [float(a) for a in splits]
                    res.min_extent = extents[:3]
                    res.max_extent = extents[3:]
                elif element == "s":
                    res.scaling = [float(a) for a in splits]
                elif element == "t":
                    res.translation = [float(a) for a in splits]
                elif element == "r":
                    res.rotation = [float(a) for a in splits]
                elif element == "m":
                    k = splits[0]
                    v: Any = ""
                    if len(splits) > 2:
                        v = tuple(splits[1:])
                    else:
                        v = splits[1]
                    if k == "tu":
                        res.translation_unit = str(v)
                    elif k == "ru":
                        res.rotation_unit = str(v)
                    else:
                        obj.meta_information[k] = v

        return res
