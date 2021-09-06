import copy
from typing import List

from geofiles.conversion.calculation import get_center, rotate_point
from geofiles.domain.geo_object_file import GeoObjectFile


class Transformer:
    """
    class used to apply different transformations to given GeoObjectFile
    """

    def rotate(self, data: GeoObjectFile) -> GeoObjectFile:
        """
        Applies the rotation defined in the given data
        :param data: to be rotated
        :return: rotated clone of the given data
        """
        return self.transform(data, scale=False, translate=False)

    def translate(self, data: GeoObjectFile) -> GeoObjectFile:
        """
        Applies the translation defined in the given data
        :param data: to be translated
        :return: rotated clone of the given data
        """
        return self.transform(data, rotate=False, scale=False)

    def scale(self, data: GeoObjectFile) -> GeoObjectFile:
        """
        Applies the scaling defined in the given data
        :param data: to be rotated
        :return: scaled clone of the given data
        """
        return self.transform(data, rotate=False, translate=False)

    @staticmethod
    def transform(
        data: GeoObjectFile,
        scale: bool = True,
        rotate: bool = True,
        translate: bool = True,
    ) -> GeoObjectFile:
        """
        Applies the scaling, rotation and translation for the given data
        :param data: to be transformed
        :param scale: Flag if scaling should be applied
        :param rotate: Flag if rotation should be applied
        :param translate: Flag if translation should be applied
        :return: transformed clone of the given data
        """
        if not data.is_origin_based():
            raise Exception("Function only supported for origin based representations")

        res = copy.deepcopy(data)
        scaling: List[float]
        if scale and res.scaling is not None:
            scaling = res.scaling
            res.scaling = None
        else:
            scaling = [1, 1, 1]

        rotation: List[float]
        if rotate and res.rotation is not None:
            rotation = res.rotation
            res.rotation = None
        else:
            rotation = [0, 0, 0]

        translation: List[float]
        if translate and res.translation is not None:
            translation = res.translation
            res.translation = None
        else:
            translation = [0, 0, 0]

        center = get_center(res.vertices)

        new_vertices = []

        zero: List[float] = [0, 0, 0]
        for vertex in res.vertices:
            # recenter around (0,0,0) and scale it
            new_vertex = [
                (v_i - c_i) * s_i for v_i, c_i, s_i in zip(vertex, center, scaling)
            ]
            rotated = rotate_point(
                new_vertex, zero, rotation[0], rotation[1], rotation[2]
            )
            # recenter around origin
            rotated = [
                c_i + r_i + t_i for c_i, r_i, t_i in zip(center, rotated, translation)
            ]
            new_vertices.append(rotated)
        res.vertices = new_vertices
        res.min_extent = []
        res.max_extent = []

        return res
