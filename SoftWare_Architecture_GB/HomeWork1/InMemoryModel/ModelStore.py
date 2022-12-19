from AmberCode.SoftWare_Architecture_GB.HomeWork1.ModelElements.Scene import Scene
from AmberCode.SoftWare_Architecture_GB.HomeWork1.ModelElements.PolygonalModel import PolygonalModel
from AmberCode.SoftWare_Architecture_GB.HomeWork1.ModelElements.Flash import Flash
from AmberCode.SoftWare_Architecture_GB.HomeWork1.ModelElements.Camera import  Camera
from AmberCode.SoftWare_Architecture_GB.HomeWork1.InMemoryModel.IModelChanger import IModelChanger
from .IModelChangedObserver import IModelChangedObserver


class ModelStore:
    # initialisation:
    def __init__(self, models: list[PolygonalModel], scenes: list[Scene], flashes: list[Flash], cameras: list[Camera], change_observers=None):
        # checking:
        if (t := type(change_observers)) not in [None, list]:
            raise Exception(f'type is wrong!')
        if t is not None:
            for change_observer in change_observers:
                if type(change_observer) is not IModelChangedObserver:
                    raise Exception(f'There cannot be non-observers elements in change_observer array...')
        if len(models) == 0:
            raise Exception(f'There must be at least one model...')
        if len(scenes) == 0:
            raise Exception(f'There must be at least one scene...')
        if len(flashes) == 0:
            raise Exception(f'There must be at least one flash...')
        if len(cameras) == 0:
            raise Exception(f'There must be at least one camera...')
        self.models = models
        self.scenes = scenes
        self.flashes = flashes
        self.cameras = cameras
        self._change_observers = change_observers

    def get_scene(self, identificator: int):
        pass

    def notify_change(self, obj: IModelChanger):
        pass



