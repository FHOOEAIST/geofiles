from abc import ABC
from io import TextIOWrapper

from geofiles.domain.geo_object import GeoObject
from geofiles.domain.geo_object_file import GeoObjectFile
from geofiles.writer.base import BaseWriter


class GeoPlyWriter(BaseWriter, ABC):
    """
    Writer implementation for creating Geo PLY geometry files (.geoply)
    """

    def _write(
        self,
        file: TextIOWrapper,
        data: GeoObjectFile,
        write_binary: bool,
        random_seed: any,
    ) -> None:
        """
        Write implementation
        :param file: target to be written
        :param data: content to be written
        :param write_binary: flag if file is a binary file
        :return:
        """
        num_vertices = len(data.vertices)
        faces = []
        for obj in data.objects:
            obj: GeoObject = obj
            for face in obj.faces:
                faces.append(face)
        num_faces = len(faces)
        self._write_to_file(file, "geoply", write_binary, True)
        self._write_to_file(file, "format ascii 1.0", write_binary, True)
        if data.crs is not None:
            self._write_to_file(file, f"crs {data.crs}", write_binary, True)

        if data.origin is not None:
            self._write_to_file(
                file,
                f"origin {' '.join([str(f) for f in data.origin])}",
                write_binary,
                True,
            )

        if data.scaling is not None:
            self._write_to_file(
                file,
                f"scale {' '.join([str(f) for f in data.scaling])}",
                write_binary,
                True,
            )

        if data.rotation is not None:
            self._write_to_file(
                file,
                f"rotate {' '.join([str(f) for f in data.rotation])}",
                write_binary,
                True,
            )

        if data.translation is not None:
            self._write_to_file(
                file,
                f"translate {' '.join([str(f) for f in data.translation])}",
                write_binary,
                True,
            )

        self._write_to_file(file, f"element vertex {num_vertices}", write_binary, True)
        self._write_to_file(file, "property float x", write_binary, True)
        self._write_to_file(file, "property float y", write_binary, True)
        self._write_to_file(file, "property float z", write_binary, True)
        self._write_to_file(file, f"element face  {num_faces}", write_binary, True)
        self._write_to_file(
            file, "property list uchar int vertex_index", write_binary, True
        )
        self._write_to_file(file, "end_header", write_binary, True)

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
        return ".geoply"

    def supports_origin_base(self) -> bool:
        """
        :return: true if file format supports origin based representation
        """
        return True
