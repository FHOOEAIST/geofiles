import math
from abc import abstractmethod, ABC
from io import TextIOWrapper

from geofiles.domain.geo_object_file import GeoObjectFile


class BaseWriter(ABC):
    def write(self, file, data: GeoObjectFile, write_binary: bool = False, append_file_type: bool = True, random_seed = None) -> None:
        """
        Allows to create write a file at the given file position
        :param file: file to be written. Either a opened file or a path to the file
        :param data: to be written
        :param write_binary: flag if file should be written in binary style (only used if file-parameter is a path)
        :param append_file_type: flag if a writer's associated file type should be appended to the given file (only if it is a path)
        :param random_seed: may be used by the writer for e.g. IDs
        :return: None
        """
        close = False
        to_write = None
        try:
            if isinstance(file, str):
                if append_file_type:
                    file += self.get_file_type()

                if write_binary:
                    to_write = open(file, 'wb')
                else:
                    to_write = open(file, 'w')
                close = True
            elif isinstance(file, TextIOWrapper):
                if not "w" in file.mode.lower:
                    raise Exception("Given file is not in write mode")

                if "b" in file.mode.lower():
                    write_binary = True
                to_write = file
            else:
                raise Exception(f"Can't handle {file}")

            self._write(to_write, data, write_binary, random_seed)

        finally:
            if close and to_write is not None:
                to_write.close()

    @abstractmethod
    def _write(self, file: TextIOWrapper, data: GeoObjectFile,  write_binary: bool, random_seed):
        """
        Write implementation
        :param file: target to be written
        :param data: content to be written
        :param write_binary: flag if file is a binary file
        :param random_seed: may be used by the writer for e.g. IDs
        :return:
        """
        return

    @abstractmethod
    def get_file_type(self) -> str:
        """
        :return: the supported file type of this writer
        """
        return ""

    def _write_to_file(self, file: TextIOWrapper, data: any, write_binary: bool, append_new_line: bool = False, encoding: str="ascii"):
        """
        Write to the given file
        :param file: to be written to
        :param data: what to be written
        :param write_binary: flag if data should be written binary ascii-encoded
        :param append_new_line: flag if new line character should be appended
        :param encoding: how data should be encoded
        :return: None
        """
        file.write(self._encode(data, write_binary, encoding))
        if append_new_line:
            file.write(self._encode("\n", write_binary, encoding))

    def _encode(self, data, write_binary: bool, encoding: str="ascii"):
        """
        Encode the given data
        :param data: to be encoded
        :param write_binary: flag if data should be encoded
        :param encoding: how data should be encoded
        :return: encoded data
        """
        if write_binary:
            return f"{data}".encode(encoding)
        else:
            return f"{data}"

    def _contains_transformation_information(self, data: GeoObjectFile):
        """
        Check the given data if it contains translation, rotation or scale information
        :param data: to be checked
        :return: NOne
        """
        if data.translation is not None:
            for t in data.translation:
                if not math.isclose(t, 0, rel_tol=1e-6):
                    raise Exception("Given data contains translation information. Transform data, before writing to file")

        if data.rotation is not None:
            for t in data.rotation:
                if not math.isclose(t, 0, rel_tol=1e-6):
                    raise Exception("Given data contains rotation information. Transform data, before writing to file")

        if data.scaling is not None:
            for t in data.scaling:
                if not math.isclose(t, 1, rel_tol=1e-6):
                    raise Exception("Given data contains scale information. Transform data, before writing to file")
