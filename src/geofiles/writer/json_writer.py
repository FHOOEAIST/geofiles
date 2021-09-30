import json
from abc import ABC, abstractmethod
from io import TextIOWrapper
from typing import Any, Dict

from geofiles.domain.geo_object_file import GeoObjectFile
from geofiles.writer.base import BaseWriter


class JsonWriter(BaseWriter, ABC):
    """
    Basic writer implementations for json based file formats
    """

    @abstractmethod
    def create_json(self, data: GeoObjectFile, random_seed: Any = None) -> Dict[Any, Any]:
        """
        Creates a json representation of the given GeoObjectFile
        """
        return dict()

    def write_to_string(
        self, data: GeoObjectFile, write_binary: bool = False, random_seed: Any = None
    ) -> str:
        return json.dumps(self.create_json(data, random_seed))

    def _write(
        self,
        file: TextIOWrapper,
        data: GeoObjectFile,
        write_binary: bool,
        random_seed: Any,
    ) -> None:
        json.dump(self.create_json(data, random_seed), file)
