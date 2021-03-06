from abc import ABC
from io import TextIOWrapper
from typing import Any, Dict

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
        if len(data.objects) != 1:
            raise Exception("GeoOFF can represent only one object. Minimize the data.")

        num_vertices = len(data.vertices)
        faces = []
        obj = data.objects[0]
        if (
            obj.contains_scaling()
            or obj.contains_rotation()
            or obj.contains_translation()
        ):
            raise Exception(
                "GeoOFF does not support local object transformation information."
            )
        for face in obj.faces:
            faces.append(face)
        num_faces = len(faces)
        origin_based = data.is_origin_based()
        contains_extent = data.contains_extent()
        contains_scaling = data.contains_scaling()
        contains_translation = data.contains_translation()
        contains_rotation = data.contains_rotation()
        if (
            data.is_geo_referenced()
            or len(obj.meta_information) != 0
            or len(data.meta_information) != 0
        ):
            header = "GeoOFF"
            if origin_based:
                header += "o"
            if contains_extent:
                header += "e"
            if contains_scaling:
                header += "s"
            if contains_translation:
                header += "t"
            if contains_rotation:
                header += "r"
            for _ in range(0, len(data.meta_information)):
                header += "f"
            for _ in range(0, len(obj.meta_information)):
                header += "m"
            self._write_to_file(file, header, write_binary, True)
            self._write_to_file(file, data.crs, write_binary, True)
            if data.origin is not None and origin_based:
                self._write_to_file(
                    file, " ".join([str(f) for f in data.origin]), write_binary, True
                )
            if (
                data.min_extent is not None
                and data.max_extent is not None
                and contains_extent
            ):
                self._write_to_file(
                    file,
                    " ".join([str(f) for f in data.min_extent])
                    + " ".join([str(f) for f in data.max_extent]),
                    write_binary,
                    True,
                )
            if data.scaling is not None and contains_scaling:
                self._write_to_file(
                    file, " ".join([str(f) for f in data.scaling]), write_binary, True
                )
            if data.translation is not None and contains_translation:
                self._write_to_file(
                    file,
                    " ".join([str(f) for f in data.translation]),
                    write_binary,
                    True,
                )
            if data.rotation is not None and contains_rotation:
                self._write_to_file(
                    file, " ".join([str(f) for f in data.rotation]), write_binary, True
                )
            self.write_meta_information(data.meta_information, file, write_binary)
            self.write_meta_information(obj.meta_information, file, write_binary)
        else:
            if origin_based:
                raise Exception("Origin information not supported in OFF file format")
            if contains_extent:
                raise Exception("Extent information not supported in OFF file format")
            if contains_scaling:
                raise Exception("Scaling information not supported in OFF file format")
            if contains_translation:
                raise Exception(
                    "Translation information not supported in OFF file format"
                )
            if contains_rotation:
                raise Exception("Rotation information not supported in OFF file format")
            if len(data.meta_information) != 0 or len(obj.meta_information) != 0:
                raise Exception("OFF file format does not support meta information")
            self._write_to_file(file, "OFF", write_binary, True)

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

    def write_meta_information(
        self, meta_information: Dict[str, Any], file: TextIOWrapper, write_binary: bool
    ) -> None:
        """
        Write the given meta information dictionary to the file
        :param meta_information: to be written
        :param file: target to be written
        :param write_binary: flag if file is a binary file
        :return:
        """
        for k, v in meta_information.items():
            if isinstance(v, tuple):
                self._write_to_file(file, f"{k} {' '.join(v)}", write_binary, True)
            else:
                self._write_to_file(file, f"{k} {v}", write_binary, True)
