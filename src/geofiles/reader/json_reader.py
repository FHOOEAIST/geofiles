import json
from abc import ABC, abstractmethod
from typing import Any, Dict, Iterable

from geofiles.domain.geo_object_file import GeoObjectFile
from geofiles.reader.base import BaseReader


class JsonReader(BaseReader, ABC):
    """
    Base class for reading json-based files
    """

    def _read(self, file: Iterable[str]) -> GeoObjectFile:
        json_file = "\n".join(file)
        loaded: Dict[Any, Any] = json.loads(json_file)

        return self.read_json(loaded)

    @abstractmethod
    def read_json(self, json_dict: Dict[Any, Any]) -> GeoObjectFile:
        """
        Read implementation for json based files
        :param json_dict: parsed json representation
        :return: Domain representation of the GeoObjectFile
        """
        return GeoObjectFile()
