from queue import PriorityQueue


def slide_puzzle(board: list[list[int]]):
    pass


def get_initial_graph():
    pass


def a_star(start, goal, graph):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {start: None}
    cost_so_far = {start: 0}

    while not frontier.empty():
        current = frontier.get()

        if current == goal:
            break

        for next in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + manhattan_heuristic(goal, next)
                frontier.put(next, priority)
                came_from[next] = current


# city blocks' distance, heuristic for finding distance between the current location of the square and its valid position
def manhattan_heuristic(coords1: list[int], coords2: list[int]):
    return abs(coords1[0] - coords2[0]) + abs(coords1[1] - coords2[1])


def some_heuristic(coords1: list[int], coords2: list[int]):
    pass


