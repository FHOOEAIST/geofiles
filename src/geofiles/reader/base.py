import re
from abc import ABC, abstractmethod
from io import TextIOWrapper
from typing import Any, Dict, Generator, Iterable, List

from geofiles.domain.face import Face
from geofiles.domain.geo_object_file import GeoObjectFile


class BaseReader(ABC):
    """
    BaseReader implementation for importing geo referenced objects
    """

    def read(self, file: Any) -> GeoObjectFile:
        """
        Reads a given file
        :param file: to be read (may be a string representing the path or an opened file instance)
        :return: Domain representation of the GeoObjectFile
        """
        close = False
        to_read: Any = None
        try:
            if isinstance(file, str):
                to_read = open(file)
                close = True
            elif isinstance(file, TextIOWrapper):
                to_read = file
            else:
                raise Exception(f"Can't handle {file}")

            return self._read(BaseReader._read_file_line(to_read))
        finally:
            if close and to_read is not None:
                to_read.close()

    def read_strings(self, input_strings: List[str]) -> GeoObjectFile:
        """
        Reads a given geometric object
        :param input_strings: strings describing a geometric object
        """
        return self._read(input_strings)

    def read_string(self, input_string: str) -> GeoObjectFile:
        """
        Reads a given geometric object
        :param input_string: string describing a geometric object
        """
        return self._read(BaseReader._split_str(input_string, "\n"))

    @staticmethod
    def _read_file_line(file: TextIOWrapper) -> Generator[str, None, None]:
        """
        Lazy function (generator) to read a file line by line
        :param file: to be read
        """
        while True:
            data = file.readline()
            if not data:
                break
            yield data

    @staticmethod
    def _split_str(string: str, sep: str = "\n") -> Generator[str, None, None]:
        """
        Lazy function (generator) to read a string line by line separated by the given sep symbol
        :param string: to be read
        """
        # warning: does not yet work if sep is a lookahead like `(?=b)`
        if sep == "":
            return (c for c in string)
        return (
            _.group(1) for _ in re.finditer(f"(?:^|{sep})((?:(?!{sep}).)*)", string)
        )

    @abstractmethod
    def _read(self, file: Iterable[str]) -> GeoObjectFile:
        """
        Read implementation
        :param file: target to be read
        :return: Domain representation of the GeoObjectFile
        """
        return GeoObjectFile()

    @staticmethod
    def _filter_faces(
        unique_vertices: bool,
        coordinate: List[Any],
        face_object: Face,
        vertex_list: List[List[Any]],
        vertex_indices: Dict[str, int],
    ) -> None:
        """
        Implementation for filtering non_unique vertices
        :param unique_vertices: Flag if vertices should be filtered
        :param coordinate: Current coordinate
        :param face_object: Current face
        :param vertex_list: List of all resulting vertices
        :param vertex_indices: Dictionary mapping already known vertices (in str representation) with their idx in the list
        :return: None
        """
        if unique_vertices:
            str_rep = "-".join([str(a) for a in coordinate])
            if not vertex_indices.get(str_rep):
                vertex_indices[str_rep] = len(vertex_list) + 1
                vertex_list.append(coordinate)

            vertex_index = vertex_indices[str_rep]
            face_object.indices.append(vertex_index + 1)
        else:
            face_object.indices.append(len(vertex_list))
            vertex_list.append(coordinate)
