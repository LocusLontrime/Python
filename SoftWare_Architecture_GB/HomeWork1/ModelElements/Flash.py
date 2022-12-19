from .Polygon import Point3D
import numpy as np
import math as m


class Flash:
    # initialisation:
    def __init__(self, location: Point3D, angle: 'Angle3D', colour: 'Colour', power: float):
        self.location = location
        self.angle = angle
        self.colour = colour
        self.power = power

    # rotate by angle:
    def rotate(self, angle: 'Angle3D'):
        self.angle.flat_angle_x += angle.flat_angle_x
        self.angle.flat_angle_y += angle.flat_angle_y
        self.angle.flat_angle_z += angle.flat_angle_z

    # move to the point:
    def move(self, point: 'Point3D'):
        self.location = point


# 3D-angle representation:
class Angle3D:
    def __init__(self, flat_angle_x: float, flat_angle_y: float, flat_angle_z: float):
        self.flat_angle_x = flat_angle_x
        self.flat_angle_y = flat_angle_y
        self.flat_angle_z = flat_angle_z
        # building a matrix of rotation:
        self.rotation_matrix = np.array([
            [m.cos(self.flat_angle_y) * m.cos(self.flat_angle_z), -m.sin(self.flat_angle_z) * m.cos(self.flat_angle_y),
             m.sin(self.flat_angle_y)],
            [m.sin(self.flat_angle_x) * m.sin(self.flat_angle_y) * m.cos(self.flat_angle_z) + m.sin(
                self.flat_angle_z) * m.cos(self.flat_angle_x),
             -m.sin(self.flat_angle_x) * m.sin(self.flat_angle_y) * m.sin(self.flat_angle_z) + m.cos(
                 self.flat_angle_x) * m.cos(self.flat_angle_z), -m.sin(self.flat_angle_x) * m.cos(self.flat_angle_y)],
            [m.sin(self.flat_angle_x) * m.sin(self.flat_angle_z) - m.sin(self.flat_angle_y) * m.cos(
                self.flat_angle_x) * m.cos(self.flat_angle_z),
             m.sin(self.flat_angle_x) * m.sin(self.flat_angle_z) + m.sin(self.flat_angle_y) * m.sin(
                 self.flat_angle_z) * m.cos(self.flat_angle_x), m.cos(self.flat_angle_x) * m.cos(self.flat_angle_y)]
        ])

    def __str__(self):
        return f'{self.flat_angle_x, self.flat_angle_y, self.flat_angle_z}'

    def __repr__(self):
        return str(self)


# covering for Colour
class Colour:
    def __init__(self, name: str):
        self.name = name
