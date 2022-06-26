import os
import random
from collections import Counter, OrderedDict
from typing import Any, Optional

from geofiles.writer.base import BaseWriter
from tests.geofiles.base_test import BaseTest


class BaseWriterTest(BaseTest):
    def get_writer(self) -> BaseWriter:  # pylint: disable=R0201
        raise NotImplementedError()

    def tearDown(self) -> None:
        writer = self.get_writer()
        if writer is not None:
            file = BaseTest.get_test_file(writer)
            if os.path.exists(file):
                os.remove(file)

    def _test_write(
        self,
        data: Any,
        ref_file_name: str,
        write_binary: bool = False,
        writer_to_use: Optional[BaseWriter] = None,
    ) -> None:
        """
        Test implementation
        :param ref_file_name: name of the reference file for comparison
        :param data: data to be written
        :param writer_to_use: Writer to be used (if None self.get_writer() is used)
        :return: None
        """
        # given
        if writer_to_use is None:
            writer: BaseWriter = self.get_writer()
        else:
            writer = writer_to_use
        file = BaseTest.get_test_file(writer)
        ref = self.get_ressource_file(ref_file_name)

        rd = random.Random()
        rd.seed(42)

        # when
        writer.write(
            file,
            data,
            write_binary,
            append_file_type=False,
            random_seed=rd.getrandbits(128),
        )

        print(file)

        # then
        self.assertTrue(os.path.exists(file))
        with open(file) as f1, open(ref) as f2:
            self.assertEqual(OrderedDict(Counter(f1)), OrderedDict(Counter(f2)))
