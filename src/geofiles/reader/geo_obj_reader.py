from abc import ABC
from typing import Iterable

from geofiles.domain.face import Face
from geofiles.domain.geo_object import GeoObject
from geofiles.domain.geo_object_file import GeoObjectFile
from geofiles.reader.base import BaseReader


class GeoObjReader(BaseReader, ABC):
    """
    Reader implementaiton for geo-referenced .obj files
    """

    def _read(self, file: Iterable[str]) -> GeoObjectFile:
        """
        Reads a given .geoobj file
        :param file: to be read (may be a string representing the path or an opened file instance)
        :return: Domain representation of the GeoObject
        """
        res = GeoObjectFile()

        current_object = GeoObject()
        last_added_object = None
        found_group = False
        filled_group = False

        for line in file:
            trimmed = line.strip()
            if not trimmed:
                continue
            trimmed = " ".join(trimmed.split())
            # check if current line is a classic vertex
            if trimmed.startswith("v "):
                coordinates = list([float(a) for a in trimmed[2:].split(" ")])
                res.vertices.append(coordinates)
            # check if current line is a face defintion
            elif trimmed.startswith("f "):
                face_defs = trimmed[2:].split(" ")
                face = Face()
                for face_def in face_defs:
                    vals = face_def.split("/")
                    list_len = len(vals)
                    if list_len > 0:
                        face.indices.append(int(vals[0]))
                    if list_len > 1 and vals[1] is not None and len(vals[1]) != 0:
                        face.texture_coordinates.append(int(vals[1]))
                    if list_len > 2:
                        face.normal_indices.append(int(vals[2]))
                current_object.faces.append(face)
                filled_group = True
            # check if current line is a group definition
            elif trimmed.startswith("g ") or trimmed.startswith("o "):
                name = trimmed[2:]
                # if it is the first group definition and if we have not found any other definition
                # just set the name of the current group; otherwise it is a new group
                if not found_group and not filled_group:
                    current_object.name = name
                else:
                    new_object = GeoObject()
                    new_object.name = name
                    new_object.parent = current_object
                    res.objects.append(current_object)
                    last_added_object = current_object
                    current_object = new_object
                found_group = True
            # check if the current line defines the coordinate reference system
            elif trimmed.startswith("crs "):
                res.crs = trimmed[4:]
            # check if the current line defines the origin
            elif trimmed.startswith("or "):
                res.origin = [float(a) for a in trimmed[3:].split(" ")]
            # check if the current line defines a file scale
            elif trimmed.startswith("sc "):
                scale = [float(a) for a in trimmed[3:].split(" ")]
                if not found_group:
                    res.scaling = scale
                else:
                    current_object.scaling = scale
            # check if the current line defines a file translation
            elif trimmed.startswith("t "):
                translation = [float(a) for a in trimmed[2:].split(" ")]
                if not found_group:
                    res.translation = translation
                else:
                    current_object.translation = translation
            # check if the current line defines a file rotation
            elif trimmed.startswith("r "):
                rotation = [float(a) for a in trimmed[2:].split(" ")]
                if not found_group:
                    res.rotation = rotation
                else:
                    current_object.rotation = rotation
            elif trimmed.startswith("e "):
                extent = [float(a) for a in trimmed[2:].split(" ")]
                res.min_extent = extent[:3]
                res.max_extent = extent[3:]
            # check if the current line defines a texture coordinate
            elif trimmed.startswith("vt "):
                coordinates = [float(a) for a in trimmed[3:].split(" ")]
                res.texture_coordinates.append(coordinates)
                filled_group = True
            # check if the current line defines a coordinate's normal
            elif trimmed.startswith("vn "):
                coordinates = [float(a) for a in trimmed[3:].split(" ")]
                res.normals.append(coordinates)
                filled_group = True

        if last_added_object is not current_object:
            res.objects.append(current_object)

        return res
