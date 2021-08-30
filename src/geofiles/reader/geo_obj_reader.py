from abc import ABC
from io import TextIOWrapper

from geofiles.domain.face import Face
from geofiles.domain.geo_object import GeoObject
from geofiles.domain.geo_object_file import GeoObjectFile
from geofiles.reader.base import BaseReader


class GeoObjReader(BaseReader, ABC):
    """
    Reader implementaiton for geo-referenced .obj files
    """

    def _read(self, file: TextIOWrapper) -> GeoObjectFile:
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

        while True:
            # Get next line from file
            line = file.readline()

            # if line is empty
            # end of file is reached
            if not line:
                break
            trimmed = line.strip()
            trimmed = " ".join(trimmed.split())
            # check if current line is a classic vertex
            if trimmed.startswith("v"):
                coordinates = trimmed[2:].split(" ")
                res.vertices.append(coordinates)
            # check if current line is a face defintion
            elif trimmed.startswith("f"):
                face_defs = trimmed[2:].split(" ")
                face = Face()
                for face_def in face_defs:
                    vals = face_def.split("/")
                    l = len(vals)
                    if l > 0:
                        face.indices.append(vals[0])
                    if l > 1 and vals[1] is not None:
                        face.texture_coordinates.append(vals[1])
                    if l > 2:
                        face.normal_indices.append(vals[2])
                current_object.faces.append(face)
                filled_group = True
            # check if current line is a group definition
            elif trimmed.startswith("g"):
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
            elif trimmed.startswith("crs"):
                res.crs = trimmed[4:]
            # check if the current line defines the origin
            elif trimmed.startswith("o"):
                res.origin = trimmed[2:].split(" ")
            elif trimmed.startswith("sc"):
                res.scaling = trimmed[3:].split(" ")
            elif trimmed.startswith("t"):
                res.translation = trimmed[2:].split(" ")
            elif trimmed.startswith("r"):
                res.rotation = trimmed[2:].split(" ")
            # check if the current line defines a texture coordinate
            elif trimmed.startswith("vt"):
                coordinates = trimmed[2:].split(" ")
                res.texture_coordinates.append(coordinates)
                filled_group = True
            # check if the current line defines a coordinate's normal
            elif trimmed.startswith("vn"):
                coordinates = trimmed[2:].split(" ")
                res.normals.append(coordinates)
                filled_group = True

        if last_added_object is not current_object:
            res.objects.append(current_object)

        return res
