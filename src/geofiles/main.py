from geofiles.conversion.local_converter import LocalConverter
from geofiles.conversion.origin_converter import OriginConverter
from geofiles.reader.geo_obj_reader import GeoObjReader
from geofiles.reader.geo_off_reader import GeoOffReader
from geofiles.reader.geo_ply_reader import GeoPlyReader
from geofiles.reader.geo_stl_reader import GeoStlReader
from geofiles.writer.city_json_writer import CityJsonWriter
from geofiles.writer.geo_json_writer import GeoJsonWriter
from geofiles.writer.geo_obj_writer import GeoObjWriter
from geofiles.conversion.crs_converter import CrsConverter

import os

from geofiles.writer.geo_off_writer import GeoOffWriter
from geofiles.writer.geo_ply_writer import GeoPlyWriter
from geofiles.writer.geo_stl_writer import GeoStlWriter
from geofiles.writer.gml_writer import GmlWriter
from geofiles.writer.kml_writer import KmlWriter

if __name__ == '__main__':
    reader = GeoPlyReader()
    cwd = os.getcwd()
    idx = cwd.find("src")
    cwd = cwd[:idx]
    path = os.path.join(os.path.join(cwd, "ressources"), "cube.ply")
    with open(path) as file:
        geoObjFile = reader.read(file)

        converter = CrsConverter()
        converted = converter.convert(geoObjFile, "urn:ogc:def:crs:OGC:2:84")

        # kml_writer = GeoPlyWriter()
        # kml_writer.write(os.path.join(os.path.join(cwd, "ressources"), "cube.ply"), converted)


        # writer = GeoObjWriter()
        # writer.write(os.path.join(os.path.join(cwd, "ressources"), "cube2.geoobj"), converted)
        # print(geoObjFile)
        #
        originconverter = OriginConverter()
        origin_based = originconverter.to_origin(converted)
        print()
        # writer.write(os.path.join(os.path.join(cwd, "ressources"), "cube3.geoobj"), origin_based)
        # non_origin_based = originconverter.from_origin(origin_based)
        # writer.write(os.path.join(os.path.join(cwd, "ressources"), "cube4.geoobj"), non_origin_based)
        #
        # localconverter = LocalConverter()
        # local = localconverter.to_local(converted)
        # writer.write(os.path.join(os.path.join(cwd, "ressources"), "local.obj"), local)
