# pylint: skip-file

"""
Size comparison using multiple obj base models.
You can find examples e.g. here: https://github.com/alecjacobson/common-3d-test-models
"""

import logging
import os
from os import listdir
from os.path import isfile, join
from typing import Dict

from geofiles.conversion.local_converter import LocalConverter
from geofiles.reader.geo_obj_reader import GeoObjReader
from geofiles.writer.base import BaseWriter
from geofiles.writer.city_json_writer import CityJsonWriter
from geofiles.writer.geo_json_writer import GeoJsonWriter
from geofiles.writer.geo_obj_writer import GeoObjWriter
from geofiles.writer.geo_off_writer import GeoOffWriter
from geofiles.writer.geo_ply_writer import GeoPlyWriter
from geofiles.writer.geo_stl_writer import GeoStlWriter
from geofiles.writer.geo_vrml_writer import GeoVrmlWriter
from geofiles.writer.gml_writer import GmlWriter
from geofiles.writer.kml_writer import KmlWriter

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    path = input("Path to sample .obj files: ")
    inputfiles = [
        f for f in listdir(path) if isfile(join(path, f)) and f.endswith(".obj")
    ]
    crs = "urn:ogc:def:crs:OGC:2:84"
    origin = [14.2842798233032, 48.30284881591775, 279.807006835938]
    reader = GeoObjReader()
    converter = LocalConverter()

    writers: Dict[str, BaseWriter] = dict()
    writers["cityjson"] = CityJsonWriter()
    writers["geojson"] = GeoJsonWriter()
    writers["geoobj"] = GeoObjWriter()
    writers["geooff"] = GeoOffWriter()
    writers["geoply"] = GeoPlyWriter()
    writers["geostl"] = GeoStlWriter()
    writers["geovrml"] = GeoVrmlWriter()
    writers["gml"] = GmlWriter()
    writers["kml"] = KmlWriter()

    encoding = dict()
    encoding["cityjson"] = False
    encoding["geojson"] = False
    encoding["geoobj"] = False
    encoding["geooff"] = False
    encoding["geoply"] = False
    encoding["geostl"] = False
    encoding["geovrml"] = False
    encoding["gml"] = True
    encoding["kml"] = True

    number_of_jobs = 0
    for value in writers.values():
        number_of_jobs += 1
        if value.supports_origin_base():
            number_of_jobs += 1
    number_of_jobs *= len(inputfiles)

    sizes = dict()
    origin_based_sizes = dict()
    done_jobs = 0
    for file in inputfiles:
        sizes_for_file = dict()
        origin_based_sizes_for_file = dict()
        geoobj = reader.read(join(path, file))
        converted = converter.from_local(geoobj, crs, origin, False)
        converted_origin_based = converter.from_local(geoobj, crs, origin, True)
        for key, value in writers.items():
            value: BaseWriter = value
            folder = join(path, key)
            os.makedirs(folder, exist_ok=True)
            target = join(folder, file)
            value.write(target, converted, encoding[key])
            done_jobs += 1
            logging.info(
                f"Step {done_jobs} of {number_of_jobs} done ({file}, {type(value).__name__})"
            )
            sizes_for_file[key] = os.path.getsize(target + value.get_file_type())
            if value.supports_origin_base():
                origin_target = join(folder, "origin_" + file)
                value.write(origin_target, converted_origin_based, encoding[key])
                done_jobs += 1
                logging.info(
                    f"Step {done_jobs} of {number_of_jobs} done ({file}, {type(value).__name__}, origin-based)"
                )
                origin_based_sizes_for_file[key] = os.path.getsize(
                    origin_target + value.get_file_type()
                )

        sizes[file] = sizes_for_file
        origin_based_sizes[file] = origin_based_sizes_for_file

    with open(join(path, "result.csv"), "w") as csvfile:
        csvfile.write("file,original")
        for extension, writer in writers.items():
            csvfile.write(f",{extension}")
            if writer.supports_origin_base():
                csvfile.write(f",{extension}-origin")
        csvfile.write("\n")

        for key, size in sizes.items():
            origin_size = origin_based_sizes[key]
            csvfile.write(key)
            csvfile.write(",")
            original_file_size = os.path.getsize(join(path, key))
            csvfile.write("{:.2f}".format(original_file_size / 1024.0))
            for file_format in writers:
                csvfile.write(",")
                csvfile.write("{:.2f}".format(size[file_format] / 1024.0))
                if origin_size.get(file_format) is not None:
                    csvfile.write(",")
                    csvfile.write("{:.2f}".format(origin_size[file_format] / 1024.0))
            csvfile.write("\n")
