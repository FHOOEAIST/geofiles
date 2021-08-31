from abc import ABC, abstractmethod
from io import TextIOWrapper

from geofiles.domain.geo_object_file import GeoObjectFile


class BaseReader(ABC):
    def read(self, file: any) -> GeoObjectFile:
        """
        Reads a given file
        :param file: to be read (may be a string representing the path or an opened file instance)
        :return: Domain representation of the GeoObjectFile
        """
        close = False
        to_read = None
        try:
            if isinstance(file, str):
                to_read = open(file)
                close = True
            elif isinstance(file, TextIOWrapper):
                to_read = file
            else:
                raise Exception(f"Can't handle {file}")

            return self._read(to_read)
        finally:
            if close and to_read is not None:
                to_read.close()

    @abstractmethod
    def _read(self, file: TextIOWrapper) -> GeoObjectFile:
        """
        Read implementation
        :param file: target to be read
        :return: Domain representation of the GeoObjectFile
        """
        return GeoObjectFile()
