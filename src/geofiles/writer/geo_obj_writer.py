from abc import ABC
from io import TextIOWrapper
from typing import Any, List

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
        if data.crs is not None:
            self._write_to_file(file, "crs ", write_binary)
            self._write_to_file(file, data.crs, write_binary, True)

        if data.is_geo_referenced() and data.origin is not None:
            self._write_to_file(
                file,
                "or " + " ".join([str(a) for a in data.origin]),
                write_binary,
                True,
            )

        if data.is_geo_referenced() and data.scaling is not None:
            self._write_to_file(
                file,
                "sc " + " ".join([str(a) for a in data.scaling]),
                write_binary,
                True,
            )

        if data.is_geo_referenced() and data.translation is not None:
            self._write_to_file(
                file,
                "t " + " ".join([str(a) for a in data.translation]),
                write_binary,
                True,
            )

        if data.is_geo_referenced() and data.rotation is not None:
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
            self._write_to_file(file, f"o {geoobject.name}", write_binary, True)
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
