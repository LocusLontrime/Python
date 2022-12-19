from .Polygon import Polygon
from .Texture import Texture


class PolygonalModel:
    # initialisation:
    def __init__(self, polygons: list[Polygon], textures=None):  # : [Texture]
        # checking:
        if (t := type(textures)) not in [None, list]:
            raise Exception(f'type is wrong!')
        if t is not None:
            for texture in textures:
                if type(texture) is not Texture:
                    raise Exception(f'There cannot be non-texture elements in textures array...')
        if len(polygons) == 0:
            raise Exception(f'There must be at least one polygon...')
        self.polygons = polygons
        self.textures = textures
