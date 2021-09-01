import copy
import math
from math import cos, pi, radians, sin
from typing import Any, List


def get_distant_point(x0: float, y0: float, d: float, theta: float) -> List[float]:
    """
    Get a new point based on the start position, distance and angle
    :param x0: start x
    :param y0: start y
    :param d: distance to new point
    :param theta: angle to new point
    :return:
    """
    theta_rad = pi / 2 - radians(theta)
    return [x0 + d * cos(theta_rad), y0 + d * sin(theta_rad)]


def get_point_distance(point1: List[Any], point2: List[Any]) -> float:
    """
    Calculates the distance between the two given points
    :param point1: first point
    :param point2: second point
    :return: distance between both points
    """
    return math.sqrt(
        sum((float(px) - float(qx)) ** 2.0 for px, qx in zip(point1, point2))
    )


def get_angle_between_points(point1: List[Any], point2: List[Any]) -> float:
    """
    Calculates the angle between two points
    :param point1: first point
    :param point2: second point
    :return: angle between both points
    """
    r = (
        180.0
        / math.pi
        * math.atan2(
            float(point2[0]) - float(point1[0]), float(point2[1]) - float(point1[1])
        )
    )

    if r < 0:
        r %= 360

    return r


def get_center(vertices: List[Any]) -> List[Any]:
    """
    Calculates the center point for the given vertices
    :param vertices: for which center should be calculated
    :return: center
    """
    if len(vertices) == 0:
        raise Exception("Given vertices are empty")

    center: List[float] = []
    cnt = 0
    for vertex in vertices:
        if len(center) == 0:
            center = copy.deepcopy(vertex)
        else:
            for idx, v in enumerate(vertex):
                center[idx] += float(v)
        cnt += 1

    for idx in range(0, len(center)):  # pylint: disable=C0200
        center[idx] /= cnt

    return center


def rotate_point(
    point: List[float],
    origin: List[float],
    roll: float,
    pitch: float,
    yaw: float,
) -> List[float]:
    """
    Rotates the given 3D point around the given origin
    :param point: to be rotated
    :param origin: rotation center
    :param roll: x-rotation
    :param pitch: y-rotation
    :param yaw: z-rotation
    :return: new point representing the rotation result
    """
    curr_x = point[0] - origin[0]
    curr_y = point[1] - origin[1]
    curr_z = point[2] - origin[2]

    r_roll = math.radians(roll)
    r_pitch = math.radians(pitch)
    r_yaw = math.radians(yaw)

    cosa = math.cos(r_yaw)
    sina = math.sin(r_yaw)
    cosb = math.cos(r_pitch)
    sinb = math.sin(r_pitch)
    cosc = math.cos(r_roll)
    sinc = math.sin(r_roll)

    axx = cosa * cosb
    axy = cosa * sinb * sinc - sina * cosc
    axz = cosa * sinb * cosc + sina * sinc
    ayx = sina * cosb
    ayy = sina * sinb * sinc + cosa * cosc
    ayz = sina * sinb * cosc - cosa * sinc
    azx = -sinb
    azy = cosb * sinc
    azz = cosb * cosc

    xr = (axx * curr_x + axy * curr_y + axz * curr_z) + origin[0]
    yr = (ayx * curr_x + ayy * curr_y + ayz * curr_z) + origin[1]
    zr = (azx * curr_x + azy * curr_y + azz * curr_z) + origin[2]

    return [xr, yr, zr]


def convert_obj_index(idx: int, list_input: Any) -> int:
    """
    Method for converting an obj based index to a python like index
    :param idx: to be converted
    :param list_input: length of referenced list or the list itself
    :return: converted idx
    """
    if idx > 0:
        return idx - 1

    list_len: int
    if isinstance(list_input, int):
        list_len = list_input
    elif isinstance(list_input, list):
        list_len = len(list_input)
    else:
        raise Exception(f"Not supported type {type(list_input)} of parameter l")

    if idx < 0:
        return list_len + idx

    raise Exception("Index 0 not supported in OBJ")
