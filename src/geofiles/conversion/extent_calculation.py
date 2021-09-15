import copy

from geofiles.conversion.origin_converter import OriginConverter
from geofiles.conversion.transformer import Transformer
from geofiles.domain.geo_object_file import GeoObjectFile


class ExtentCalculator:
    """
    Class which allows to calculate the geographical extents of a GeoObjectFile
    """

    @staticmethod
    def update_extent(
        data: GeoObjectFile,
        include_transformation: bool = False,
        geospatial_extent: bool = False,
        bearing_offset: float = 0.0,
    ) -> GeoObjectFile:
        """
        Updates the min and max extent values of this geo-referenced object file, also considering transformation information and origin-based representation
        :param data: Data to be updated
        :param include_transformation: If true transformation information is considered for the extent information
        :param geospatial_extent: Flag if extent should be georeferenced or contain local coordinates
        :param bearing_offset: Used for conversion (required when geospatial_extent == True or include_transformation == True)
        :returns: Updated data
        """
        origin_converter = OriginConverter()
        origin_based = data.is_origin_based()
        copied_data = copy.deepcopy(data)

        if include_transformation:
            # transformation requires origin based data, so convert the data to origin based
            if not origin_based:
                temp = origin_converter.to_origin(
                    copied_data, bearing_offset=bearing_offset
                )
            else:
                temp = copied_data

            transformer = Transformer()
            transformed = transformer.transform(temp, True, True, True, True)
            if origin_based and not geospatial_extent:
                copied_data.min_extent = transformed.min_extent
                copied_data.max_extent = transformed.max_extent
                return copied_data

            origin = origin_converter.from_origin(
                transformed, bearing_offset=bearing_offset, update_extent=True
            )
            data.min_extent = origin.min_extent
            data.max_extent = origin.max_extent
            return data

        if origin_based and geospatial_extent:  # global origin + global extents
            converted = origin_converter.from_origin(data, bearing_offset, True)
            data.min_extent = converted.min_extent
            data.max_extent = converted.max_extent
        else:  # global coordinates + global extents
            data.update_extent()

        return data
