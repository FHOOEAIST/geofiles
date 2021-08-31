import math
from abc import ABC
from io import TextIOWrapper

from geofiles.conversion.calculation import convert_obj_index
from geofiles.conversion.static import get_wgs_84
from geofiles.domain.face import Face
from geofiles.domain.geo_object import GeoObject
from geofiles.domain.geo_object_file import GeoObjectFile
from geofiles.writer.base import BaseWriter


class GeoVrmlWriter(BaseWriter, ABC):
    """
    Writer implementation for creating Geo-Referenced VRML geometry files (.wrl)
    """

    def _write(
        self, file: TextIOWrapper, data: GeoObjectFile, write_binary: bool, random_seed
    ):
        """
        Write implementation
        :param file: target to be written
        :param data: content to be written
        :param write_binary: flag if file is a binary file
        :return:
        """
        if data.crs != get_wgs_84():
            raise Exception("This writer implementation requires WGS:84 coordinate system")

        if write_binary:
            self._write_to_file(file, "#VRML V2.0 ascii", write_binary, True)
        else:
            self._write_to_file(file, "#VRML V2.0 utf8", write_binary, True)

        self._write_to_file(file, "EXTERNPROTO GeoCoordinate [", write_binary, True)
        self._write_to_file(file, " field SFNode geoOrigin # NULL", write_binary, True)
        self._write_to_file(file, ' field MFString geoSystem # [ "GDC" ]', write_binary, True)
        self._write_to_file(file, " field MFString point # []", write_binary, True)
        self._write_to_file(file, " field MFString point # []", write_binary, True)
        self._write_to_file(file, '] [ "urn:web3d:geovrml:1.0/protos/GeoCoordinate.wrl"', write_binary, True)
        self._write_to_file(file, ' "file:///C|/Program%20Files/GeoVRML/1.0/protos/GeoCoordinate.wrl"', write_binary, True)
        self._write_to_file(file, ' "http://www.geovrml.org/1.0/protos/GeoCoordinate.wrl" ]', write_binary, True)

        if data.is_origin_based():
            self._write_to_file(file, "EXTERNPROTO GeoOrigin [", write_binary, True)
            self._write_to_file(file, '            exposedField  MFString  geoSystem    # [ "GDC" ]', write_binary, True)
            self._write_to_file(file, '            exposedField  SFString  geoCoords    # ""', write_binary, True)
            self._write_to_file(file, '          ] [ "urn:web3d:geovrml:1.0/protos/GeoOrigin.wrl"', write_binary, True)
            self._write_to_file(file, '	      "file:///C|/Program%20Files/GeoVRML/1.0/protos/GeoOrigin.wrl"', write_binary, True)
            self._write_to_file(file, '	      "http://www.geovrml.org/1.0/protos/GeoOrigin.wrl" ]', write_binary, True)

            origin = " ".join([str(a) for a in data.origin])
            self._write_to_file(file, "DEF ORIGIN GeoOrigin {", write_binary, True)
            self._write_to_file(file, '   geoSystem ["GDC"]', write_binary, True)
            self._write_to_file(file, f'   geoCoords "{origin}"', write_binary, True)
            self._write_to_file(file, "}", write_binary, True)


        num_of_vertices = len(data.vertices)
        num_of_objects = len(data.objects)
        i = 0

        contains_transform = data.scaling is not None or data.rotation is not None or data.translation is not None

        for obj in data.objects:
            obj: GeoObject = obj
            local_vertices = []
            vertex_mapping = dict()
            for face in obj.faces:
                face: Face = face
                for idx in face.indices:
                    vertex_mapping[idx] = len(local_vertices)
                    local_vertices.append(data.get_vertex(idx))

            if contains_transform:
                self._write_to_file(file, f"DEF OBJECT-{i} Shape "+"{", write_binary, True)
            else:
                self._write_to_file(file, f"Shape "+"{", write_binary, True)
            self._write_to_file(file, "   geometry IndexedFaceSet {", write_binary, True)
            self._write_to_file(file, f"      coord GeoCoordinate " + "{", write_binary, True)
            self._write_to_file(file, '         geoSystem [ "GDC" ]', write_binary, True)
            if data.is_origin_based():
                self._write_to_file(file, '         geoOrigin', write_binary, True)
                self._write_to_file(file, '           USE ORIGIN ', write_binary, True)

            self._write_to_file(file, '         point [', write_binary, True)
            for vertex in local_vertices:
                self._write_to_file(file, '            ', write_binary, False)
                for coord in vertex:
                    self._write_to_file(file, f"{coord} ", write_binary, False)
                self._write_to_file(file, '', write_binary, True)
            self._write_to_file(file, '         ]', write_binary, True)
            self._write_to_file(file, '      }', write_binary, True)
            self._write_to_file(file, '      coordIndex [', write_binary, False)

            num_of_faces = len(obj.faces)
            j = 0
            for face in obj.faces:
                face: Face = face
                for idx in face.indices:
                    self._write_to_file(file, f'{convert_obj_index(idx, num_of_vertices)} ', write_binary, False)
                self._write_to_file(file, '-1', write_binary, False)
                if j < num_of_faces - 1:
                    self._write_to_file(file, ', ', write_binary, False)
                j += 1

            self._write_to_file(file, ']', write_binary, True)
            self._write_to_file(file, "   }", write_binary, True)
            self._write_to_file(file, "}", write_binary, True)
            i += 1

        if data.scaling is not None:
            self._write_to_file(file, "Transform { ", write_binary, True)
            scale = " ".join([str(a) for a in data.scaling])
            self._write_to_file(file, f"   scale {scale}", write_binary, True)
            self._print_children(num_of_objects, file, write_binary)
            self._write_to_file(file, "}", write_binary, True)

        if data.rotation is not None:
            for idx, rotation in enumerate(data.rotation):
                self._write_to_file(file, "Transform { ", write_binary, True)
                rotation = math.radians(rotation)
                if idx == 0:
                    axis = "1 0 0"
                elif idx == 1:
                    axis = "0 1 0"
                else:
                    axis = "0 0 0"

                if not math.isclose(rotation, 0):
                    self._write_to_file(file, f"   rotation {axis} {rotation}", write_binary, True)
                    self._print_children(num_of_objects, file, write_binary)
                    self._write_to_file(file, "}", write_binary, True)

        if data.translation is not None:
            self._write_to_file(file, "Transform { ", write_binary, True)
            translation = " ".join([str(a) for a in data.translation])
            self._write_to_file(file, f"   translation {translation}", write_binary, True)
            self._print_children(num_of_objects, file, write_binary)
            self._write_to_file(file, "}", write_binary, True)

    def get_file_type(self) -> str:
        """
        :return: the supported file type of this writer
        """
        return ".wrl"

    def _print_children(self, num_of_objects: int, file: TextIOWrapper, write_binary: bool):
        """
        Prints the children definition for a transform element
        :param num_of_objects: number of objects
        :param file: target to be written
        :param write_binary: flag if file is a binary file
        :return: None
        """
        self._write_to_file(file, f"   children [", write_binary, True)
        for i in range(0, num_of_objects):
            self._write_to_file(file, f"      USE OBJECT-{i}", write_binary, True)
        self._write_to_file(file, f"   ]", write_binary, True)