# A* algorithm
import heapq
# Used https://www.geeksforgeeks.org/dsa/a-search-algorithm/ for
# reference/information gathering

import math

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
    if 0 > src[0] > width or 0 > src[1] > height:
        raise Exception("Invalid source position! Source must be within grid!")
    if 0 > dest[0] > width or 0 > dest[1] > height:
        raise Exception("Invalid destination position! Destination must be within grid!")

    # Make sure that source does not start in destination (not an error)
    if src == dest:
        return

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

        closed_list[to_index(pos, width)] = True  # Mark cell as visited
        cost_list[to_index(pos, width)] = (cell[0], cell[2]) # Mark cost of cell

        # Check all valid neighbors to the cell
        for i in h.directions:
            new_pos = (pos[0] + i[0], pos[1] + i[1])

            # Checks if cell is valid
            if 0 > new_pos[0] > width or 0 > new_pos[1] > height:
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

                return path





