import math
from abc import ABC, abstractmethod
from io import StringIO, TextIOWrapper
from typing import Any, Union

from geofiles.domain.geo_object_file import GeoObjectFile


class BaseWriter(ABC):
    """
    Base implementation for writing geo-referenced object
    """

    def write(
        self,
        file: Any,
        data: GeoObjectFile,
        write_binary: bool = False,
        append_file_type: bool = True,
        random_seed: Any = None,
    ) -> None:
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
        to_write: Any = None
        try:
            if isinstance(file, str):
                if append_file_type:
                    file += self.get_file_type()

                if write_binary:
                    to_write = open(file, "wb")
                else:
                    to_write = open(file, "w")
                close = True
            elif isinstance(file, TextIOWrapper):
                if "w" not in file.mode.lower():
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
    def _write(
        self,
        file: Union[TextIOWrapper, StringIO],
        data: GeoObjectFile,
        write_binary: bool,
        random_seed: Any,
    ) -> None:
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

    def write_to_string(
        self, data: GeoObjectFile, write_binary: bool = False, random_seed: Any = None
    ) -> str:
        """
        Write to string implementation
        :param data: content to be written
        :param write_binary: flag if file should be written in binary style (only used if file-parameter is a path)
        :param random_seed: may be used by the writer for e.g. IDs
        :return:
        """
        to_write = StringIO("")
        self._write(to_write, data, write_binary, random_seed)
        to_write.seek(0)
        return "".join(to_write.readlines())

    def supports_origin_base(self) -> bool:  # pylint: disable=R0201
        """
        :return: true if file format supports origin based representation
        """
        return False

    def _write_to_file(
        self,
        file: Union[TextIOWrapper, StringIO],
        data: Any,
        write_binary: bool,
        append_new_line: bool = False,
        encoding: str = "ascii",
    ) -> None:
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

    @staticmethod
    def _encode(data: Any, write_binary: bool, encoding: str = "ascii") -> Any:
        """
        Encode the given data
        :param data: to be encoded
        :param write_binary: flag if data should be encoded
        :param encoding: how data should be encoded
        :return: encoded data
        """
        if write_binary:
            return str(data).encode(encoding)
        return f"{data}"

    @staticmethod
    def _contains_transformation_information(data: GeoObjectFile) -> None:
        """
        Check the given data if it contains translation, rotation or scale information
        :param data: to be checked
        :return: None
        """
        if data.translation is not None:
            for t in data.translation:
                if not math.isclose(float(t), 0, rel_tol=1e-6):
                    raise Exception(
                        "Given data contains translation information. Transform data, before writing to file"
                    )

        if data.rotation is not None:
            for t in data.rotation:
                if not math.isclose(float(t), 0, rel_tol=1e-6):
                    raise Exception(
                        "Given data contains rotation information. Transform data, before writing to file"
                    )

        if data.scaling is not None:
            for t in data.scaling:
                if not math.isclose(float(t), 1, rel_tol=1e-6):
                    raise Exception(
                        "Given data contains scale information. Transform data, before writing to file"
                    )
