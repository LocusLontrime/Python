# accepted on codewars.com
import heapq
import random
import time

import numpy as np
# direction components:
directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
# max integer among grid heights:
MAX_VAL = 9


def aux_path_finder(area: list[list['Node']]):
    if len(area) == 0 or len(area[0]) == 0:
        return []
    start, finish = (0, 0), (len(area) - 1, len(area[0]) - 1)
    path, min_rounds = a_star(area, area[finish[0]][finish[1]], area[start[0]][start[1]])
    print(f'path: {path}')
    return min_rounds


# the main method:
def path_finder(area: str):  # 36 366 98 989 LL
    # print(f'area:\n{area}')
    # a-star implementation:
    if len(area) == 0:
        return []
    # recovering grid from blueprint:
    grid_of_nodes, start, finish = make_grid_from_blueprint(area)
    # path finding:
    path, min_rounds = a_star(grid_of_nodes, grid_of_nodes[finish[0]][finish[1]], grid_of_nodes[start[0]][start[1]])
    print(f'path: {path}')
    return min_rounds


# convenient for task heuristic length:
def manhattan_heuristic(node1: 'Node', node2: 'Node'):
    return abs(node1.position.y - node2.position.y) + abs(node1.position.x - node2.position.x)


# the core:
def a_star(grid: list[list['Node']], start: 'Node', finish: 'Node'):
    nodes_to_be_visited = [start]
    start.g = 0
    heapq.heapify(nodes_to_be_visited)
    # main cycle's steps counter:
    iterations = 0
    # queue cycle:
    while nodes_to_be_visited:
        curr_node = heapq.heappop(nodes_to_be_visited)
        iterations += 1
        # print(f'{iterations}-th iteration, curr_node: {curr_node.position, curr_node.val}')
        # stop condition:
        if curr_node == finish:
            break
        # neighbours for further visiting:
        for neigh in get_adjacent_ones(grid, curr_node):
            if neigh.g > curr_node.g + abs(neigh.val - curr_node.val):
                neigh.g = curr_node.g + abs(neigh.val - curr_node.val)
                neigh.h = manhattan_heuristic(neigh, finish)
                neigh.previously_visited_node = curr_node
                heapq.heappush(nodes_to_be_visited, neigh)
    # the beginning node for path restoring:
    node = finish
    shortest_path = []
    # path restoring (here we get the reversed path) -->> just for visualisation:
    while node.previously_visited_node:
        shortest_path.append(node)
        node = node.previously_visited_node
    # start point adding
    shortest_path.append(start)
    # returning path and min climbing rounds value
    return list(shortest_path), finish.g


# finds possible neighs for the current cell:
def get_adjacent_ones(grid: list[list['Node']], node: 'Node'):
    list_of_adj_nodes = []
    y, x = node.position.y, node.position.x
    for (j, i) in directions:
        neigh_j, neigh_i = y + j, x + i
        if 0 <= neigh_j < len(grid) and 0 <= neigh_i < len(grid[0]):
            neigh = grid[neigh_j][neigh_i]
            list_of_adj_nodes.append(neigh)
    return list_of_adj_nodes


# simple class for Node's coordinate pair representation
class Point:
    def __init__(self, y, x):
        self.y = y
        self.x = x

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f'({self.y},{self.x})'


# class, describing the node's signature
class Node:
    def __init__(self, y, x, val=0):
        self.position = Point(y, x)  # (2,5)
        self.val = val
        self.previously_visited_node = None  # for building the shortest path of Nodes from the starting point to the ending one

        self.g = np.Infinity  # aggregated cost of moving from start to the current Node, Infinity chosen for convenience and algorithm's logic
        self.h = 0  # approximated cost evaluated by heuristic for path starting from the current node and ending at the exit Node
        # f = h + g or total cost of the current Node is not needed here

    def __eq__(self, other):
        return self.position == other.position

    # this is needed for using Node objects in priority queue like heapq and so on
    def __lt__(self, other):
        return self.h + MAX_VAL * self.g < other.h + MAX_VAL * other.g  # the right sigh is "<" for __lt__() method

    def __str__(self):
        return str(self.val)

    def __repr__(self):
        return str(self.val)


# makes a grid from a blueprint given
def make_grid_from_blueprint(blueprint: str):
    enters_q = blueprint.count('\n')
    length = len(blueprint)
    x_max, y_max = (length - 1) // (enters_q + 1) + 1, enters_q + 1
    print(f'y_max, x_max: {y_max, x_max - 1}')
    grid = []
    # filling:
    for y in range(y_max):
        grid.append([])
        for x in range(x_max - (1 if enters_q > 0 else 0)):
            iterator = y * x_max + x
            ch = blueprint[iterator]
            if ch.isdigit():
                grid[y].append(Node(y, x, int(ch)))
    # returning data:
    return grid, (0, 0), (y_max - 1, x_max - 1 - (1 if enters_q > 0 else 0))


def make_grid_of_nodes(j_max, i_max):
    grid = []
    for j in range(j_max):
        grid.append([])
        for i in range(i_max):
            grid[j].append(Node(j, i, random.randrange(1, MAX_VAL + 1)))
    return grid


f = "\n".join([
    "777000",
    "007000",
    "007000",
    "007000",
    "007000",
    "007777"
])

g = "\n".join([
    "000000",
    "000000",
    "000000",
    "000010",
    "000109",
    "001010"
])

k = '898'

big = "\n".join([
    '40312153318463928389124693335526276903288737770959',
    '06734772523765687867431783825625998719467190802499',
    '70121970630214416589066997374464998482389941340857',
    '64223374638545608692808221239336147400330891306888',
    '25231299154555477627653035792224658231950481903045',
    '83290716029796934761374183700526477216981338666290',
    '99361655518573069040775687170180030302795022518029',
    '76271281123759804261620058871149841662467920839859',
    '08044277345421822417599194292976110930801663653039',
    '56759506183661662588800183295544346532597404889675',
    '95211388783672665945362254154268880465137202223784',
    '51142859752461775106070630165352617126779746529839',
    '01478728756450931934759573171647566082180272148517',
    '24662329159465095064919800140808305957471619830095',
    '19614458206738017251504146374642083819643032386852',
    '10042902002831708612498644621704556196834381867737',
    '39497061379426638292878999338182862358950657875483',
    '92588121389775190284246406041665205205389649249867',
    '76197115341874082261134314925543506549450317287974',
    '29994178111658530615933925052181970031834472657533',
    '14963680792351897998433758701690945889108556567085',
    '92192903088560684179101219420026349444905906393299',
    '13590964068124552565555863837415175183391453287120',
    '45432370368660473651219199419014004006560671145329',
    '36126183915468248368478621395533362169754483376201',
    '53160660646222379698697401411293017372786326825171',
    '74882911408419991803248545287808678285644982765730',
    '68551684847332180736093008105799254364112041579852',
    '45676331881703785385534491757826357350267838221152',
    '80300466928724148306422433948521173714704386001257',
    '00813687913224795584380426266046824225020453141775',
    '26301018777053286588821470449178724451795306685732',
    '80082486955705096389149391893729935878780155272566',
    '95493644300620158297758798196064085942974065020541',
    '79285165054869379598525203078180442125115251602790',
    '34370081459990453059022437433456560061213877679400',
    '72335412062995355317486580292831603747003155069015',
    '60787787837842739085081827966973922134068841619419',
    '28051834310207713501131543897373843530104429634168',
    '87337500802894814007062603522382159200110039234529',
    '04435353417256400117268695023029071320365512484230',
    '22668427171084740233597753420104210220874257775878',
    '37771422172339452436336284701619196430892707810968',
    '75071738200365620683334843788105348449323214557289',
    '88832426587903959454491273509776809585027215606178',
    '56500949970749626109982849224066598914811839623241',
    '84809187669145579259806311266682798186469733416866',
    '18739929772636035967138126461700959749979627158357',
    '33824500532502954787901024678418416897838402258748',
    '08622481833846333128343968984145977638943896009475'
])

fail = '\n'.join([
    '444079',
    '771076',
    '915737',
    '330054',
    '318663',
    '436765'
])

grid_made = make_grid_of_nodes(1000, 1000)

start = time.time_ns()
print(aux_path_finder(grid_made))
finish = time.time_ns()
print(f'time elapsed: {(finish - start) // 10 ** 6} milliseconds')


