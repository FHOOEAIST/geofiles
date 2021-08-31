import copy
import math
from math import cos, pi, radians, sin


def get_distant_point(x0: float, y0: float, d: float, theta: float) -> list:
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


def get_point_distance(point1: list, point2: list) -> float:
    """
    Calculates the distance between the two given points
    :param point1: first point
    :param point2: second point
    :return: distance between both points
    """
    return math.sqrt(sum((float(px) - float(qx)) ** 2.0 for px, qx in zip(point1, point2)))


def get_angle_between_points(point1: list, point2: list) -> float:
    """
    Calculates the angle between two points
    :param point1: first point
    :param point2: second point
    :return: angle between both points
    """
    r = 180.0 / math.pi * math.atan2(float(point2[0]) - float(point1[0]), float(point2[1]) - float(point1[1]))

    if r < 0:
        r %= 360

    return r


def get_center(vertices: list) -> list:
    """
    Calculates the center point for the given vertices
    :param vertices: for which center should be calculated
    :return: center
    """
    if len(vertices) == 0:
        raise Exception("Given vertices are empty")

    center = None
    cnt = 0
    for vertex in vertices:
        if center is None:
            center = copy.deepcopy(vertex)
        else:
            for idx, v in enumerate(vertex):
                center[idx] += float(v)
        cnt += 1

    for idx in range(0, len(center)):
        center[idx] /= cnt

    return center


def rotate_point(
    point: list, origin: list, roll: float, pitch: float, yaw: float
) -> list:
    """
    Rotates the given 3D point around the given origin
    :param point: to be rotated
    :param origin: rotation center
    :param roll: x-rotation
    :param pitch: y-rotation
    :param yaw: z-rotation
    :return: new point representing the rotation result
    """
    currX = point[0] - origin[0]
    currY = point[1] - origin[1]
    currZ = point[2] - origin[2]

    rRoll = math.radians(roll)
    rPitch = math.radians(pitch)
    rYaw = math.radians(yaw)

    cosa = math.cos(rYaw)
    sina = math.sin(rYaw)
    cosb = math.cos(rPitch)
    sinb = math.sin(rPitch)
    cosc = math.cos(rRoll)
    sinc = math.sin(rRoll)

    axx = cosa * cosb
    axy = cosa * sinb * sinc - sina * cosc
    axz = cosa * sinb * cosc + sina * sinc
    ayx = sina * cosb
    ayy = sina * sinb * sinc + cosa * cosc
    ayz = sina * sinb * cosc - cosa * sinc
    azx = -sinb
    azy = cosb * sinc
    azz = cosb * cosc

    xR = (axx * currX + axy * currY + axz * currZ) + origin[0]
    yR = (ayx * currX + ayy * currY + ayz * currZ) + origin[1]
    zR = (azx * currX + azy * currY + azz * currZ) + origin[2]

    return [xR, yR, zR]


def convert_obj_index(idx: int, l: any) -> int:
    """
    Method for converting an obj based index to a python like index
    :param idx: to be converted
    :param l: length of referenced list or the list itself
    :return: converted idx
    """
    if isinstance(l, int):
        list_len = l
    elif isinstance(l, list):
        list_len = len(l)
    else:
        raise Exception(f"Not supported type {type(l)} of parameter l")

    if idx > 0:
        return idx - 1
    elif idx < 0:
        return list_len + idx
    else:
        raise Exception("Index 0 not supported in OBJ")
