import os
from os import listdir
from os.path import isfile, join

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

if __name__ == '__main__':
    """
    Size comparison using multiple obj base models.
    You can find examples e.g. here: https://github.com/alecjacobson/common-3d-test-models
    """
    path = r"C:\Users\P41743\Desktop\samples"  # input("Path to sample .obj files: ")
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    crs = "urn:ogc:def:crs:OGC:2:84"
    origin = [14.2842798233032, 48.30284881591775, 279.807006835938]
    reader = GeoObjReader()
    converter = LocalConverter()

    writers = dict()
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

    sizes = dict()
    origin_based_sizes = dict()
    for file in onlyfiles:
        print(file)
        sizes_for_file = dict()
        origin_based_sizes_for_file = dict()
        geoobj = reader.read(join(path, file))
        converted = converter.from_local(geoobj, crs, origin, False)
        converted_origin_based = converter.from_local(geoobj, crs, origin, True)
        for key, value in writers.items():
            print(f"---- {type(value)}")
            value: BaseWriter = value
            folder = join(path, key)
            os.makedirs(folder, exist_ok=True)
            target = join(folder, file)
            value.write(target, converted, encoding[key])
            sizes_for_file[key] = os.path.getsize(target+value.get_file_type())
            if value.supports_origin_base():
                origin_target = join(folder, "origin_" + file)
                value.write(origin_target, converted_origin_based, encoding[key])
                origin_based_sizes_for_file[key] = os.path.getsize(origin_target + value.get_file_type())

        sizes[file] = sizes_for_file
        origin_based_sizes[file] = origin_based_sizes_for_file

    print("-----------------------------------------------------------------")

    formats = ["cityjson","geojson","geoobj","geooff","geoply","geostl","geovrml","gml","kml"]
    num_of_formats = len(formats)
    print("File,cityjson,geojson,geoobj,geooff,geoply,geostl,geovrml,gml,kml")
    for key, size in sizes.items():
        origin_size = origin_based_sizes[key]
        s = f"{key},"
        for idx, file_format in enumerate(formats):
            s += "{:.2f}".format(size[file_format] / 1024.0)
            if origin_size.get(file_format) is not None:
                s += " | "
                s += "{:.2f}".format(origin_size[file_format] / 1024.0)
            if idx < num_of_formats - 1:
                s += ","
        print(s)


