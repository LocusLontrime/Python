from .PolygonalModel import PolygonalModel
from .Flash import Flash
from .Camera import Camera


class Scene:
    # initialisation:
    def __init__(self, identificator: int, models: list[PolygonalModel], cameras: list[Camera], flashes=None):
        # checking:
        if (t := type(flashes)) not in [None, list]:
            raise Exception(f'type is wrong!')
        if t is not None:
            for flash in flashes:
                if type(flash) is not Flash:
                    raise Exception(f'There cannot be non-flash elements in Flashes array...')
        if len(models) == 0:
            raise Exception(f'There must be at least one model...')
        if len(cameras) == 0:
            raise Exception(f'There must be at least one camera...')
        self.id = identificator
        self.models = models
        self.cameras = cameras
        self.flashes = flashes


    # two "empty" methods:
    def method1(self, something):
        ...

    def method2(self, something1, something2):
        if type(something1) != type(something2):
            raise Exception(f'types must be the same...')
        ...
