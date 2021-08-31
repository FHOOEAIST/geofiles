def get_wgs_84() -> str:
    """
    :return: name of the WGS 84 coordinate system
    """
    return "urn:ogc:def:crs:OGC:2:84"


def get_epsg_4326() -> str:
    """
    :return: name of the EPSG 4326 coordinate system
    """
    return "urn:ogc:def:crs:EPSG::4326"


def get_lon_lat(vertex: list, coordinate_system: str) -> tuple:
    """
    Method for accessing longitude and latitude
    :param vertex: WGS84 or EPSG4236 vertex
    :param coordinate_system: coordinate system of the vertex
    :return: longitude, latitude
    """
    if coordinate_system == get_wgs_84():
        return vertex[0], vertex[1]
    elif coordinate_system == get_epsg_4326():
        return vertex[1], vertex[0]
    else:
        raise Exception(f"Not supported crs {coordinate_system}")
