from abc import ABC
from io import TextIOWrapper

from geofiles.domain.geo_object import GeoObject
from geofiles.domain.geo_object_file import GeoObjectFile
from geofiles.writer.base import BaseWriter


class GeoStlWriter(BaseWriter, ABC):
    """
    Writer implementation for creating Geo-Referenced STL geometry files (.geostl)
    """

    def __init__(self) -> None:
        self.stl_name = ""

    def _write(
        self, file: TextIOWrapper, data: GeoObjectFile, write_binary: bool, random_seed: any
    ) -> None:
        """
        Write implementation
        :param file: target to be written
        :param data: content to be written
        :param write_binary: flag if file is a binary file
        :return:
        """
        self._contains_transformation_information(data)

        origin = ""
        if data.is_origin_based():
            for c in data.origin:
                origin += str(c) + " "
        self._write_to_file(
            file, f"geosolid {data.crs} {origin} {self.stl_name}", write_binary, True
        )
        for obj in data.objects:
            obj: GeoObject = obj
            for face in obj.faces:
                if len(face.normal_indices) != 0:
                    normal = [0, 0, 0]
                    for idx in face.normal_indices:
                        n = data.get_normal(idx)
                        normal = [x + y for x, y in zip(normal, n)]
                    normal = [str(x / len(face.normal_indices)) for x in normal]

                    self._write_to_file(
                        file, f" facet normal {' '.join(normal)}", write_binary, True
                    )
                else:
                    self._write_to_file(file, f" facet", write_binary, True)
                self._write_to_file(file, f"  outer loop", write_binary, True)
                for idx in face.indices:
                    vertex = [str(a) for a in data.get_vertex(idx)]
                    self._write_to_file(
                        file, f"   vertex {' '.join(vertex)}", write_binary, True
                    )
                self._write_to_file(file, f"  endloop", write_binary, True)
                self._write_to_file(file, f" endfacet", write_binary, True)

        self._write_to_file(file, "endgeosolid", write_binary, True)

    def get_file_type(self) -> str:
        """
        :return: the supported file type of this writer
        """
        return ".geostl"
