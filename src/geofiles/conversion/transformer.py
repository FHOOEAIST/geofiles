import copy
from typing import Dict, List

from geofiles.conversion.calculation import convert_obj_index, get_center, rotate_point
from geofiles.domain.face import Face
from geofiles.domain.geo_object_file import GeoObjectFile


class Transformer:
    """
    class used to apply different transformations to given GeoObjectFile
    """

    def rotate(
        self,
        data: GeoObjectFile,
        update_extents: bool = False,
        apply_only_global: bool = True,
    ) -> GeoObjectFile:
        """
        Applies the rotation defined in the given data
        :param data: to be rotated
        :param update_extents: Flag if extents of result should be re-calculated
        :param apply_only_global: Flag that decides if only global transformations should be applied or also local ones
        :return: rotated clone of the given data
        """
        return self.transform(
            data,
            scale=False,
            translate=False,
            update_extents=update_extents,
            apply_only_global=apply_only_global,
        )

    def translate(
        self,
        data: GeoObjectFile,
        update_extents: bool = False,
        apply_only_global: bool = True,
    ) -> GeoObjectFile:
        """
        Applies the translation defined in the given data
        :param data: to be translated
        :param update_extents: Flag if extents of result should be re-calculated
        :param apply_only_global: Flag that decides if only global transformations should be applied or also local ones
        :return: rotated clone of the given data
        """
        return self.transform(
            data,
            rotate=False,
            scale=False,
            update_extents=update_extents,
            apply_only_global=apply_only_global,
        )

    def scale(
        self,
        data: GeoObjectFile,
        update_extents: bool = False,
        apply_only_global: bool = True,
    ) -> GeoObjectFile:
        """
        Applies the scaling defined in the given data
        :param data: to be rotated
        :param update_extents: Flag if extents of result should be re-calculated
        :param apply_only_global: Flag that decides if only global transformations should be applied or also local ones
        :return: scaled clone of the given data
        """
        return self.transform(
            data,
            rotate=False,
            translate=False,
            update_extents=update_extents,
            apply_only_global=apply_only_global,
        )

    @staticmethod
    def transform(
        data: GeoObjectFile,
        scale: bool = True,
        rotate: bool = True,
        translate: bool = True,
        update_extents: bool = False,
        apply_only_global: bool = True,
    ) -> GeoObjectFile:
        """
        Applies the scaling, rotation and translation for the given data
        :param data: to be transformed
        :param scale: Flag if scaling should be applied
        :param rotate: Flag if rotation should be applied
        :param translate: Flag if translation should be applied
        :param update_extents: Flag if extents of result should be re-calculated
        :param apply_only_global: Flag that decides if only global transformations should be applied or also local ones
        :return: transformed clone of the given data
        """
        if not data.is_origin_based():
            raise Exception("Function only supported for origin based representations")

        if not data.is_default_rotation_unit():
            raise Exception(
                "Function only supported for rotation information using degrees (deg)"
            )

        if not data.is_default_translation_unit():
            raise Exception(
                "Function only supported for translation information using metres (m)"
            )

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

        for vertex in res.vertices:
            new_vertices.append(
                Transformer._transform_vertex(
                    vertex, center, scaling, rotation, translation
                )
            )
        res.vertices = new_vertices

        if not apply_only_global:
            center = get_center(res.vertices)
            vertex_index_mapping: Dict[str, int] = dict()
            transformed_vertices = []
            counter = 1
            for geoobj in res.objects:
                if (
                    geoobj.contains_translation()
                    or geoobj.contains_rotation()
                    or geoobj.contains_translation()
                ):
                    if geoobj.translation is not None and geoobj.contains_translation():
                        local_translation = geoobj.translation
                        geoobj.translation = None
                    else:
                        local_translation = [0, 0, 0]

                    if geoobj.rotation is not None and geoobj.contains_rotation():
                        local_rotation = geoobj.rotation
                        geoobj.rotation = None
                    else:
                        local_rotation = [0, 0, 0]

                    if geoobj.scaling is not None and geoobj.contains_scaling():
                        local_scaling = geoobj.scaling
                        geoobj.scaling = None
                    else:
                        local_scaling = [1, 1, 1]
                    new_faces = []
                    for face in geoobj.faces:
                        new_face = Face()
                        for idx in face.indices:
                            vertex = res.vertices[convert_obj_index(idx, res.vertices)]
                            transformed = Transformer._transform_vertex(
                                vertex,
                                center,
                                local_scaling,
                                local_rotation,
                                local_translation,
                            )
                            string_representation = " ".join(
                                [str(a) for a in transformed]
                            )
                            if vertex_index_mapping.get(string_representation) is None:
                                vertex_index_mapping[string_representation] = counter
                                transformed_vertices.append(transformed)
                                counter += 1
                            new_face.indices.append(
                                vertex_index_mapping[string_representation]
                            )
                        new_faces.append(new_face)
                    geoobj.faces = new_faces
                else:
                    new_faces = []
                    for face in geoobj.faces:
                        new_face = Face()
                        for idx in face.indices:
                            vertex = res.vertices[convert_obj_index(idx, res.vertices)]
                            string_representation = " ".join([str(a) for a in vertex])
                            if vertex_index_mapping.get(string_representation) is None:
                                vertex_index_mapping[string_representation] = counter
                                transformed_vertices.append(vertex)
                                counter += 1
                            new_face.indices.append(
                                vertex_index_mapping[string_representation]
                            )
                        new_faces.append(new_face)
                    geoobj.faces = new_faces
            res.vertices = transformed_vertices

        res.min_extent = []
        res.max_extent = []
        if update_extents:
            res.update_extent()

        return res

    @staticmethod
    def _transform_vertex(
        vertex: List[float],
        center: List[float],
        scaling: List[float],
        rotation: List[float],
        translation: List[float],
    ) -> List[float]:
        """
        Transforms the given vertex using the params
        :param center: Center of all vertices
        :param scaling: To be applied
        :param rotation: To be applied
        :param translation: To be applied
        :returns: transformed vertex
        """
        # recenter around (0,0,0) and scale it
        new_vertex = [
            (v_i - c_i) * s_i for v_i, c_i, s_i in zip(vertex, center, scaling)
        ]
        rotated = rotate_point(
            new_vertex, [0, 0, 0], rotation[0], rotation[1], rotation[2]
        )
        # recenter around origin
        rotated = [
            c_i + r_i + t_i for c_i, r_i, t_i in zip(center, rotated, translation)
        ]
        return rotated
