from abc import ABC
from io import TextIOWrapper
from typing import Any

from geofiles.domain.geo_object_file import GeoObjectFile
from geofiles.writer.base import BaseWriter


class GeoOffWriter(BaseWriter, ABC):
    """
    Writer implementation for creating Geo-Referenced OFF geometry files (.geooff)
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
        self._contains_transformation_information(data)

        num_vertices = len(data.vertices)
        faces = []
        for obj in data.objects:
            for face in obj.faces:
                faces.append(face)
        num_faces = len(faces)
        if data.is_geo_referenced():
            self._write_to_file(file, "GeoOFF", write_binary, True)
        else:
            self._write_to_file(file, "OFF", write_binary, True)

        if data.crs is not None and data.origin is None:
            self._write_to_file(file, data.crs, write_binary, True)
        elif data.origin is not None and data.origin is not None:
            self._write_to_file(
                file,
                f"{data.crs} {' '.join([str(f) for f in data.origin])}",
                write_binary,
                True,
            )
        self._write_to_file(file, f"{num_vertices} {num_faces} 0", write_binary, True)

        for v in data.vertices:
            self._write_to_file(file, " ".join([str(f) for f in v]), write_binary, True)
        for face in faces:
            s = ""
            for f in face.indices:
                s += " "
                f = int(f)
                if f > 0:
                    s += str(f - 1)
                else:
                    s += str(num_vertices - f)
            self._write_to_file(file, f"{len(face.indices)}{s}", write_binary, True)

    def get_file_type(self) -> str:
        """
        :return: the supported file type of this writer
        """
        return ".geooff"

    def supports_origin_base(self) -> bool:
        """
        :return: true if file format supports origin based representation
        """
        return True
