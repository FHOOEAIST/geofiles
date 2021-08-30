import os
from collections import OrderedDict, Counter
import random

from geofiles.writer.base import BaseWriter
from tests.geofiles.base_test import BaseTest


class BaseWriterTest(BaseTest):
    def get_writer(self):
        return None

    def tearDown(self):
        writer = self.get_writer()
        if writer is not None:
            file = BaseTest.get_test_file(writer)
            if os.path.exists(file):
                os.remove(file)

    def _test_write(self, data, ref_file_name:str, write_binary:bool = False):
        """
        Test implementation
        :param ref_file_name: name of the reference file for comparison
        :param data:
        :return:
        """
        # given
        writer: BaseWriter = self.get_writer()
        file = BaseTest.get_test_file(writer)
        ref = self.get_ressource_file(ref_file_name)

        rd = random.Random()
        rd.seed(42)

        # when
        writer.write(file, data, write_binary, append_file_type=False, random_seed=rd.getrandbits(128))

        # then
        self.assertTrue(os.path.exists(file))
        with open(file) as f1, open(ref) as f2:
            self.assertEqual(OrderedDict(Counter(f1)), OrderedDict(Counter(f2)))
