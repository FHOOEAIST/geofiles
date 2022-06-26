from typing import Any, Iterable, List, Optional


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


def get_lon_lat(vertex: List[float], coordinate_system: str) -> List[float]:
    """
    Method for accessing longitude and latitude
    :param vertex: WGS84 or EPSG4236 vertex
    :param coordinate_system: coordinate system of the vertex
    :return: longitude, latitude
    """
    if coordinate_system == get_wgs_84():
        return [vertex[0], vertex[1]]

    if coordinate_system == get_epsg_4326():
        return [vertex[1], vertex[0]]

    raise Exception(f"Not supported crs {coordinate_system}")


def update_min_max(
    vertex: List[float],
    min_extent: Optional[List[float]],
    max_extent: Optional[List[float]],
) -> None:
    """
    Update the min and max extent information based on the vertex
    :param vertex: input
    :param min_extent: current min extent
    :param max_extent: current max extent
    :return: None
    """
    if min_extent is None or max_extent is None:
        return

    for idx, elem in enumerate(vertex):
        min_value = min_extent[idx]
        max_value = max_extent[idx]
        if min_value is None or elem < min_value:
            min_extent[idx] = elem
        if max_value is None or elem > max_value:
            max_extent[idx] = elem


def is_not_none_nor_empty(to_check: Optional[List[Any]]) -> bool:
    """
    Checks if the given optional list is neither None nor empty
    :param to_check: List to be checked
    :results: true if list is not none and list is not empty
    """
    return to_check is not None and len(to_check) > 0


def pairwise(iterable: Iterable[Any]) -> Any:
    """
    Method for a pairwise access of an iterable
    :param iterable: to be iterated
    :returns: (x, y) pairs of iterable
    """

    a = iter(iterable)
    return zip(a, a)


def triplewise(iterable: Iterable[Any]) -> Any:
    """
    Method for a triplewise access of an iterable
    :param iterable: to be iterated
    :returns: (x, y) pairs of iterable
    """
    a = iter(iterable)
    return zip(a, a, a)
