import math


class Polygon:
    # initialisation:
    def __init__(self, points: list):
        for point in points:
            if type(point) is not Point3D:
                raise Exception(f'Cannot create polygon with non-Point3D elements...')
        # triangle is the minimum possible polygon:
        if len(points) < 3:
            raise Exception(f'Cannot create polygon with two or less vertices...')
        # for convenience:
        self.points = list(sorted(points, key=lambda p: (p.x, p.y, p.z)))
        print(f'{self}')

    def __str__(self):
        s = ''
        for point in self.points:
            s += f'{str(point)} '
        return s

    def __repr__(self):
        return str(self)


# just a 3D-point representation:
class Point3D:
    # initialisation:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def get_distance_3d(self, other) -> float:
        # Cartesian distance:
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2)

    # equality:
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    # inequality:
    def __ne__(self, other):
        return not(self == other)

    def __str__(self):
        return f'({self.x, self.y, self.z})'

    def __repr__(self):
        return f'({self.x, self.y, self.z})'

    # 2 methods that make class object iterable:
    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        i = self.index
        self.index += 1
        return i




# point1 = Point3D(98, 989, 98989)
# point2 = Point3D(98, 989, 1000000)
# point3 = Point3D(1, 1, 100)
# t = [point1, point2, point3]
# polygon = Polygon(t)

