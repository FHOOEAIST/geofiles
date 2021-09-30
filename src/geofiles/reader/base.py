import re
from abc import ABC, abstractmethod
from io import TextIOWrapper
from typing import Any, Generator, Iterable, List

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
