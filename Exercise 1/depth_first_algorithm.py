import math
import warnings
from dataclasses import dataclass


# Different Heuristics functions

# Manhattan distance is to be used when we are only allowed to
# move in four directions (left, right, up, down)
class Manhattan:
    def __new__(cls, *args, **kwargs):
        raise TypeError("Manhattan is static-only")

    @staticmethod
    def distance(cur, goal):
        return abs(cur[0] - goal[0]) + abs(cur[1] - goal[1])

    directions = ((-1, 0), (0, 1), (1, 0), (0, -1))

# Diagonal distance is to be used when we are allowed to move
# in eight directions
class Diagonal:
    def __new__(cls, *args, **kwargs):
        raise TypeError("Diagonal is static-only")

    @staticmethod
    def distance(cur, goal, D=1, D2=math.sqrt(2)):
        dx = abs(cur[0] - goal[0])
        dy = abs(cur[1] - goal[1])
        return D * (dx + dy) + (D2 - 2 * D) * min(dx, dy)

    directions = ((-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1))

# Euclidian distance is to be used when we are allowed to
# move in any direction (any angle)
class Euclidean:
    def __new__(cls, *args, **kwargs):
        raise TypeError("Euclidean is static-only")

    @staticmethod
    def distance(cur, goal):
        return math.sqrt((cur[0] - goal[0])**2 + (cur[1] - goal[1])**2)

    directions = ((-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1))



@dataclass(order=True)
class Node:
    # Position
    pos: tuple[int, int]

    # Cost
    g: float
    # h: float

    # Pointer leading back to source
    parent: "Node | None" = None

def search(grid, src, dest, algorithm=Manhattan, iterations=0):
    if type(grid) != list or grid is None or len(grid) == 0 or len(grid[0]) == 0:
        raise Exception("Grid needs to be an 2 dimensional list!")

    height, width = len(grid), len(grid[0])
    iterations = width * height if iterations == 0 else iterations

    # Makes sure that the grid map is valid
    if not all(len(row) == width for row in grid):
        raise Exception("Invalid grid size! Grid must be a rectangle!")

    # Checks if src & dest are valid
    if not (0 <= src[0] < width and 0 <= src[1] < height):
        raise Exception("Invalid source position! Source must be within grid!")
    if not (0 <= dest[0] < width and 0 <= dest[1] < height):
        raise Exception("Invalid destination position! Destination must be within grid!")

    # Make sure that source does not start in destination (not an error)
    if src == dest:
        return src, 0

    node = Node(src, 0, None) # Source node

    # Add list that marks points in grid that
    node_list: list[list[Node | None]] = [[None for _ in range(width)] for _ in range(height)]

    while True:
        # Breaks the loop if node is None
        if node is None:
            warnings.warn("No solution found!")
            return None, -1

        node_list[node.pos[1]][node.pos[0]] = node

        # Breaks the loop if iteration limit is exceeded
        if iterations == 0:
            warnings.warn("Ran out of iterations! Did not find a solution!")
            return None, -1
        iterations -= 1

        _node = None

        # Check all valid neighbors to the cell
        for direction in algorithm.directions:
            _pos = (node.pos[0] + direction[0], node.pos[1] + direction[1])

            # Checks if cell is valid
            if not (0 <= _pos[0] < width and 0 <= _pos[1] < height):
                continue

            # Check if node has not been checked already
            if node_list[_pos[1]][_pos[0]] is not None:
                continue

            # Ignore all other directions if a valid direction
            # is found
            g = grid[_pos[1]][_pos[0]] + node.g
            _node = Node(_pos, g, node)
            break

        # If no direction was valid then backtrack
        node = node.parent if _node is None else _node

        if node.pos == dest:

            # Make list with path from dest -> src (temp)
            path = []
            next_node = _node
            while next_node is not None:
                path.append(next_node.pos)
                next_node = next_node.parent
            path.reverse()  # Reverse src -> dest
            # path = [(x, y) for y, x in reversed(path)]  # Reverse src -> dest and (row, col) -> (x, y)

            return path, node.g


