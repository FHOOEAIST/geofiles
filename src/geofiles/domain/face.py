class Face:
    """
    Class that represents an individual face
    """

    def __init__(self):
        """
        Initializes a face with the following attributes:
        - indices: The indices of all vertices that represent the polygonal boundary of this face
        - normal_indices: The indices of the normals of this face
        - texture_coordinates: Indices of the the texture_coordinates of this face

        Note that indices use the obj ordering with start index 1 and indexes < 0 for tail access (so -1 == vertices[len(vertices)-1]
        """
        self.indices = []
        self.normal_indices = []
        self.texture_coordinates = []
