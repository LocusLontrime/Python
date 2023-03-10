import functools
import inspect


def change_detection(cls):
    """ Decorator for get_change of class attributes """

    cls_attrs_list = [
        key for key in cls.__dict__.keys() if
        not callable(getattr(cls, key))
        and not key.startswith("__")
    ]

    obj = None

    # inner decorator for getting exemplar's methods
    def deco(func):
        nonlocal obj

        @functools.wraps(func)
        def _wrapper(*args, **kwargs):
            nonlocal obj
            obj = args[0]  # <<-- self
            f = func(*args, **kwargs)
            obj_attrs_list = [
                key for key in obj.__dict__.keys() if
                not callable(getattr(obj, key))
                and key != 'name'
            ]
            print(f'self dict: {obj_attrs_list}')

            for obj_attr in obj_attrs_list:
                ...

            return f

        return _wrapper

    init_m = getattr(cls, '__init__')
    setattr(cls, '__init__', deco(init_m))

    print(f'cls_attrs_list: {cls_attrs_list}')

    return cls


@change_detection
class Struct:
    # class vars:
    THRESHOLD = 989
    SECRET_NUM = 35666

    # initialization of object-related vars:
    def __init__(self, name='', y=0):
        self.name = name
        self.y = y
        self.max_y = 98


# s = Struct('Structure', 98989)

class T:
    def __init__(self, y=989):
        self._x = 98
        self.y = y
        # self.y.__dict__['change'] = 'init'

    @property
    def x(self):
        return self._x

    # def __getattribute__(self, item):
    #     return getattr(self.y, item)


t = T()


def func(x_):
    return x_ ** 2


t.x.__dict__['change'] = None
setattr(t.x, 'change', func)

t.x.change()


# print(f't: {t}')

# print(f'property: {t.y.state}')

# TODO: getattr from Lutz!


class Catcher:
    def __getattr__(self, item):
        print(f'Get: {item}')

    def __setattr__(self, key, value):
        print(f'Set: {key, value}')


# X = Catcher()
# X.job
# X.pay
# X.pay = 99

# print(f'X.job: {X.job}')
# print(f'X.n: {X.n}')


# def full_algo():
#     def perform_edge_relaxation(node1: Node, node2: Node) -> None:
#         self._iterations += 1
#         if node1.g != np.Infinity and node1.g + node1.val < node2.g:
#             print(f'node: {node1}')
#             node2.g = node1.g + node1.val
#             node2.times_visited += 1
#             node2.previously_visited_node = node1
#             if node2.times_visited == 1:
#                 node2.type = NodeType.VISITED_NODE
#             else:
#                 node2.type = NodeType.TWICE_VISITED
#             node2.update_sprite_colour()
#             # print(f'node: {node2}, colour: {NodeType[node2.type.value]}')
#             # relaxation been completed:
#             self.flag = True
#
#
#     # starting point:
#     self._obj.start_node.g = 0
#     # cycling through all vertices - 1:
#     for i in range(self._obj.tiles_q * self._obj.hor_tiles_q - 1):
#         self.flag = False
#         # horizontal links:
#         for y in range(self._obj.tiles_q):
#             for x in range(self._obj.hor_tiles_q - 1):
#                 n1, n2 = self._obj.grid[y][x], self._obj.grid[y][x + 1]
#                 if n2.type != NodeType.WALL:
#                     perform_edge_relaxation(n1, n2)
#         # vertical links:
#         for y in range(self._obj.tiles_q - 1):
#             for x in range(self._obj.hor_tiles_q):
#                 n1, n2 = self._obj.grid[y][x], self._obj.grid[y + 1][x]
#                 if n2.type != NodeType.WALL:
#                     perform_edge_relaxation(n1, n2)
#         # check for negative cycle! BEFORE PATH RECOVERING!
#         if not self.flag:
#             # early path-recovering:
#             self.recover_path()
#             break
#     # if the path has not been restored:
#     self.recover_path()
