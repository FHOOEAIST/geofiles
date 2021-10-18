import json
import re
from abc import ABC, abstractmethod
from io import TextIOWrapper
from typing import Any, Generator, Iterable, List, Dict

from geofiles.domain.geo_object_file import GeoObjectFile
from geofiles.reader.base import BaseReader


class JsonReader(BaseReader, ABC):
    def _read(self, file: Iterable[str]) -> GeoObjectFile:
        json_file = "\n".join(file)
        loaded: dict = json.loads(json_file)

        return self._read_json(loaded)

    @abstractmethod
    def _read_json(self, json_dict: Dict[Any, Any]) -> GeoObjectFile:
        """
        Read implementation for json based files
        :param json_dict: parsed json representation
        :return: Domain representation of the GeoObjectFile
        """
        return GeoObjectFile()
