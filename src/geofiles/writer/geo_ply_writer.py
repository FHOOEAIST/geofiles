from abc import ABC
from io import TextIOWrapper
from typing import Any

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
        random_seed: Any,
    ) -> None:
        """
        Write implementation
        :param file: target to be written
        :param data: content to be written
        :param write_binary: flag if file is a binary file
        :return:
        """
        if len(data.objects) != 1:
            raise Exception("GeoPLY can represent only one object. Minimize the data.")

        num_vertices = len(data.vertices)
        faces = []
        for obj in data.objects:
            if (
                obj.contains_scaling()
                or obj.contains_rotation()
                or obj.contains_translation()
            ):
                raise Exception(
                    "GeoPLY does not support local object transformation information."
                )
            for face in obj.faces:
                faces.append(face)
        num_faces = len(faces)
        if data.is_geo_referenced():
            self._write_to_file(file, "geoply", write_binary, True)
        else:
            self._write_to_file(file, "ply", write_binary, True)

        self._write_to_file(file, "format ascii 1.0", write_binary, True)
        if data.is_geo_referenced() and data.crs is not None:
            self._write_to_file(file, f"crs {data.crs}", write_binary, True)

        if data.is_geo_referenced() and data.origin is not None:
            self._write_to_file(
                file,
                f"origin {' '.join([str(f) for f in data.origin])}",
                write_binary,
                True,
            )

        if data.is_geo_referenced() and data.scaling is not None:
            self._write_to_file(
                file,
                f"scale {' '.join([str(f) for f in data.scaling])}",
                write_binary,
                True,
            )

        if data.is_geo_referenced() and data.rotation is not None:
            self._write_to_file(
                file,
                f"rotate {' '.join([str(f) for f in data.rotation])}",
                write_binary,
                True,
            )

        if data.is_geo_referenced() and data.translation is not None:
            self._write_to_file(
                file,
                f"translate {' '.join([str(f) for f in data.translation])}",
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
                "extent "
                + " ".join([str(a) for a in data.min_extent])
                + " "
                + " ".join([str(a) for a in data.max_extent]),
                write_binary,
                True,
            )
        if not data.is_default_translation_unit():
            self._write_to_file(file, f"tu {data.translation_unit}", write_binary, True)

        if not data.is_default_rotation_unit():
            self._write_to_file(file, f"ru {data.rotation_unit}", write_binary, True)

        for k, v in data.objects[0].meta_information:
            if type(v) is tuple:
                to_write = f"{' '.join(v)}"
            else:
                to_write = f"{v}"
            self._write_to_file(file, f"meta {k} {to_write}", write_binary, True)

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
