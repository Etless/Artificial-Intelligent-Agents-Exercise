# Used https://www.geeksforgeeks.org/dsa/a-search-algorithm/ for
# reference/information gathering
import heapq
import math
import warnings

import numpy as np


# Used to convert X, Y positions to array index
def to_index(i, width)->int:
    return i[0] + i[1] * width

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



# Grid is an 1D array made 2D by using the width variable.
# The 3D is the "cost" which can be thought of as a "height"
def a_star_search(grid, width, src, dest, h=Manhattan, iterations=0):
    iterations = len(grid) if iterations == 0 else iterations
    height = len(grid) // width

    # Makes sure that the grid map is valid
    if height != len(grid) / width:
        raise Exception("Invalid grid size! Grid must be square!")

    # Checks if src & dest are valid
    if 0 < src[0] >= width or 0 < src[1] >= height:
        raise Exception("Invalid source position! Source must be within grid!")
    if 0 < dest[0] >= width or 0 < dest[1] >= height:
        raise Exception("Invalid destination position! Destination must be within grid!")

    # Make sure that source does not start in destination (not an error)
    if src == dest:
        return src

    # The heap containing all "possible" moves. When the heap is writen to
    # heapq is used to quickly sort it depending on the cost
    open_heap = []
    heapq.heappush(open_heap, (0.0, src, src)) # Add src

    # List of visited cells/positions. Used to remove overlapping
    closed_list = [False] * len(grid)

    # List of cost. Only shows the visited cells positions. It also
    # contains the parent cell which it came from
    cost_list = [math.inf, (0, 0)] * len(grid)

    while True:
        # Breaks the loop if iteration limit is exceeded
        if iterations == 0:
            raise Exception("Ran out of iterations! Did not find a solution!")
        iterations -= 1

        # Breaks the loop if heap is empty
        if len(open_heap) == 0:
            raise Exception("No solution found!")

        # Get the lowest cost cell
        cell = heapq.heappop(open_heap)
        pos = cell[1]

        # Checks if cell is already closed
        if closed_list[to_index(pos, width)]:
            continue

        closed_list[to_index(pos, width)] = True  # Mark cell as visited
        cost_list[to_index(pos, width)] = (cell[0], cell[2]) # Mark cost of cell

        # Check all valid neighbors to the cell
        for i in h.directions:
            new_pos = (pos[0] + i[0], pos[1] + i[1])

            # Checks if cell is valid
            if 0 < new_pos[0] >= width or 0 > new_pos[1] >= height:
                continue

            # Checks if cell is already closed
            if closed_list[to_index(new_pos, width)]:
                continue

            # Calculate the total cost of the cell
            cost = h.distance(new_pos, dest) + grid[to_index(new_pos, width)]
            heapq.heappush(open_heap, (cost, new_pos, pos))  # Add new positon to heap

            # Check if cell is at destination
            if new_pos == dest:
                closed_list[to_index(new_pos, width)] = True
                cost_list[to_index(new_pos, width)] = (cost, pos)

                # Make list with path from dest -> src (temp)
                path = [dest]
                while path[-1] != src:
                    path.append(cost_list[path[-1][0] + path[-1][1] * width][1])
                path.reverse() # Reverse src -> dest

                print(cost_list)

                return path


def test(grid, src, dest, algorithm=Manhattan, iterations=0):
    height, width  = grid.shape[0], grid.shape[1]
    iterations = width * height if iterations == 0 else iterations

    # Makes sure that the grid map is valid
    if grid.ndim != 2 or width == 0 or height == 0:
        raise Exception("Invalid grid size! Grid must be a rectangle!")

    # Flip (x, y) to (row, column) to match numpy
    src = (src[1], src[0])
    dest = (dest[1], dest[0])

    # Checks if src & dest are valid
    if 0 < src[1] >= width or 0 < src[0] >= height:
        raise Exception("Invalid source position! Source must be within grid!")
    if 0 < dest[1] >= width or 0 < dest[0] >= height:
        raise Exception("Invalid destination position! Destination must be within grid!")

    # Make sure that source does not start in destination (not an error)
    if src == dest:
        return src[1], src[0]  # (row, col) -> (x, y)

    # The heap containing all "possible" moves. heapq is used when
    # writing to quickly sort it depending on the cost
    open_list = []
    heapq.heappush(open_list, (0.0, src, src))  # Add src (pos, dest, parent)

    # List of visited cells/positions. Used to remove overlapping
    closed_list = np.zeros((height, width), dtype=bool)

    # List of cost. Only shows for visited cells positions
    cost_list = np.empty((height, width), dtype=float)

    # List of initialized neighbor. Shows what cell activated it.
    # Used to generate path at the end
    path_list = np.empty((height, width, 2), dtype=int)

    while True:
        # Breaks the loop if iteration limit is exceeded
        if iterations == 0:
            warnings.warn("Ran out of iterations! Did not find a solution!")
            return None
        iterations -= 1

        # Breaks the loop if heap is empty
        if len(open_list) == 0:
            warnings.warn("No solution found!")
            return None

        # Get the lowest cost cell
        cost, pos, parent = heapq.heappop(open_list)
        print(cost)
        # Checks if cell is already closed
        if closed_list[pos]:
            continue

        closed_list[pos] = True  # Mark cell as visited
        cost_list[pos] = cost # Mark cost of cell
        path_list[pos] = parent # Mark parent at cell

        # Check all valid neighbors to the cell
        for i in algorithm.directions:
            new_pos = (pos[0] + i[0], pos[1] + i[1])

            # Checks if cell is valid
            if 0 < new_pos[1] >= width or 0 > new_pos[0] >= height:
                continue

            # Calculate the total cost of the cell
            _cost = algorithm.distance(new_pos, dest) + grid[new_pos] + cost
            heapq.heappush(open_list, (_cost, new_pos, pos))  # Add new positon to heap

            # Check if cell is at destination
            if new_pos == dest:
                # Pretty print options
                np.set_printoptions(
                    precision=2,  # number of decimal places for floats
                    suppress=True,  # suppress scientific notation
                    linewidth=80,  # max characters per line
                    threshold=100  # max elements before summarizing
                )

                print(cost_list)
                # Make list with path from dest -> src (temp)
                path = [dest, pos]
                while not np.array_equal(path[-1], src):
                    path.append((int(path_list[path[-1][0], path[-1][1], 0]), int(path_list[path[-1][0], path[-1][1], 1])))
                #path.reverse()  # Reverse src -> dest
                path = [(x, y) for y, x in reversed(path)] # Reverse src -> dest and (row, col) -> (x, y)

                return path




