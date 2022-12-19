from .Polygon import Point3D
from .Flash import Angle3D

class Camera:
    # initialisation:
    def __init__(self, location: Point3D, angle: 'Angle3D'):
        self.location = location
        self.angle = angle

    # rotate by angle:
    def rotate(self, angle: 'Angle3D'):
        self.angle.flat_angle_x += angle.flat_angle_x
        self.angle.flat_angle_y += angle.flat_angle_y
        self.angle.flat_angle_z += angle.flat_angle_z

    # move to the point:
    def move(self, point: 'Point3D'):
        self.location = point