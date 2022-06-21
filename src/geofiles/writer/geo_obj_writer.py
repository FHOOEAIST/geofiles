from abc import ABC
from io import TextIOWrapper
from typing import Any, List

from geofiles.domain.geo_object import GeoObject
from geofiles.domain.geo_object_file import GeoObjectFile
from geofiles.writer.base import BaseWriter


class GeoObjWriter(BaseWriter, ABC):
    """
    Class for writing Geo-Referenced .obj files (.geoobj)
    """

    def _write(
        self,
        file: TextIOWrapper,
        data: GeoObjectFile,
        write_binary: bool,
        random_seed: Any,
    ) -> None:
        """
        Write implementation
        :param file: target to be written
        :param data: content to be written
        :param write_binary: flag if file is a binary file
        :return:
        """
        geo_referenced = data.is_geo_referenced()
        if data.crs is not None:
            self._write_to_file(file, "crs ", write_binary)
            self._write_to_file(file, data.crs, write_binary, True)

        if geo_referenced and data.origin is not None:
            self._write_to_file(
                file,
                "or " + " ".join([str(a) for a in data.origin]),
                write_binary,
                True,
            )

        if geo_referenced and data.scaling is not None:
            self._write_to_file(
                file,
                "sc " + " ".join([str(a) for a in data.scaling]),
                write_binary,
                True,
            )

        if geo_referenced and data.translation is not None:
            self._write_to_file(
                file,
                "t " + " ".join([str(a) for a in data.translation]),
                write_binary,
                True,
            )

        if geo_referenced and data.rotation is not None:
            self._write_to_file(
                file,
                "r " + " ".join([str(a) for a in data.rotation]),
                write_binary,
                True,
            )

        if (
            data.contains_extent()
            and data.min_extent is not None
            and data.max_extent is not None
        ):
            self._write_to_file(
                file,
                "e "
                + " ".join([str(a) for a in data.min_extent])
                + " "
                + " ".join([str(a) for a in data.max_extent]),
                write_binary,
                True,
            )

        self._write_coordinates(data.vertices, file, "v ", write_binary)
        self._write_coordinates(data.normals, file, "vn ", write_binary)
        self._write_coordinates(data.texture_coordinates, file, "vt ", write_binary)

        for geoobject in data.objects:
            if len(geoobject.faces) == 0:
                self._write_to_file(file, f"g {geoobject.name}", write_binary, True)
            else:
                self._write_to_file(file, f"o {geoobject.name}", write_binary, True)

            if geo_referenced:
                self._write_transformation(geoobject, file, write_binary)
            for k, v in geoobject.meta_information.items():
                if type(v) is tuple:
                    to_write = ' '.join(v)
                else:
                    to_write = str(v)
                self._write_to_file(file, f"m {k} {to_write}", write_binary, True)

            for f in geoobject.faces:
                self._write_to_file(file, "f ", write_binary)
                contains_textures = len(f.texture_coordinates) != 0
                contains_normals = len(f.normal_indices) != 0
                index_len = len(f.indices)
                for i, idx in enumerate(f.indices):
                    self._write_to_file(file, idx, write_binary)

                    if contains_textures or contains_normals:
                        self._write_to_file(file, "/", write_binary)

                    if contains_textures:
                        self._write_to_file(
                            file, f.texture_coordinates[i], write_binary
                        )

                    if contains_normals:
                        self._write_to_file(file, "/", write_binary)
                        self._write_to_file(file, f.normal_indices[i], write_binary)

                    if i < index_len - 1:
                        self._write_to_file(file, " ", write_binary)

                self._write_to_file(file, "", write_binary, True)

    def _write_transformation(
        self, geoobj: GeoObject, file: TextIOWrapper, write_binary: bool
    ) -> None:
        """
        Write the transformation information of the geoobject to the file
        :param geoobj: for which transformation should be written
        :param file: to which the coordinate will be written
        :param write_binary: check if ascii mode is used
        :return:
        """
        if geoobj.scaling is not None and geoobj.contains_scaling():
            self._write_to_file(
                file,
                "sc " + " ".join([str(a) for a in geoobj.scaling]),
                write_binary,
                True,
            )

        if geoobj.translation is not None and geoobj.contains_translation():
            self._write_to_file(
                file,
                "t " + " ".join([str(a) for a in geoobj.translation]),
                write_binary,
                True,
            )

        if geoobj.rotation is not None and geoobj.contains_rotation():
            self._write_to_file(
                file,
                "r " + " ".join([str(a) for a in geoobj.rotation]),
                write_binary,
                True,
            )

    def _write_coordinates(
        self,
        coordinates: List[List[Any]],
        file: TextIOWrapper,
        prefix: str,
        write_binary: bool,
    ) -> None:
        """
        Write the given coordinates to the file
        :param coordinates: to be written
        :param file: to which the coordinate will be written
        :param prefix: used to identify the coordinate type
        :param write_binary: check if ascii mode is used
        :return:
        """
        for v in coordinates:
            self._write_to_file(file, prefix, write_binary)
            self._write_to_file(file, " ".join([str(a) for a in v]), write_binary)
            self._write_to_file(file, "", write_binary, True)

    def get_file_type(self) -> str:
        """
        :return: the supported file type of this writer
        """
        return ".geoobj"

    def supports_origin_base(self) -> bool:
        """
        :return: true if file format supports origin based representation
        """
        return True
