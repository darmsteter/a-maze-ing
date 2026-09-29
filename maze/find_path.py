from heapq import heappush, heappop
from typing import Callable

from maze.models import Cell, DIRECTIONS


def maze_counter() -> Callable[[], int]:
    """Create a counter function that returns an incrementing integer.

    Returns:
        A function that returns the next integer each time it is called.
    """

    count = 0

    def counter() -> int:
        nonlocal count
        count += 1
        return count

    return counter


def manhattan_distance(x1: int, x2: int, y1: int, y2: int) -> int:
    """Calculate the Manhattan distance between two points.

    Args:
        x1: X-coordinate of the first point.
        x2: X-coordinate of the second point.
        y1: Y-coordinate of the first point.
        y2: Y-coordinate of the second point.

    Returns:
        The Manhattan distance between the two points.
    """

    return abs(x1 - x2) + abs(y1 - y2)


def update_neighbours(
    cell: Cell,
    frontier: list[tuple[int, int, tuple[int, int]]],
    g_score: dict[tuple[int, int], int],
    exit: tuple[int, int],
    counter: Callable[[], int],
    came_from: dict[tuple[int, int], tuple[int, int]],
) -> None:
    """Update pathfinding information for the accessible neighbours of a cell.

    Neighbours with a shorter path from the entry are added to the
    priority queue with their estimated total cost.

    Args:
        cell: Current cell whose neighbours are being checked.
        frontier: Priority queue containing cells to be explored.
        g_score: Dictionary storing the cost of the shortest known path
            from the entry to each cell.
        exit: Coordinates of the maze exit.
        counter: Function returning a unique incrementing number for
            priority queue tie-breaking.
        came_from: Dictionary storing the previous cell for each cell
            in the current path.
    """

    walls = (cell.top, cell.right, cell.bottom, cell.left)
    for direction, dir_x, dir_y in DIRECTIONS:
        if walls[direction]:
            continue

        neighbour = (cell.x + dir_x, cell.y + dir_y)
        tentative_g_score = g_score[(cell.x, cell.y)] + 1
        if neighbour not in g_score or tentative_g_score < g_score[neighbour]:
            g_score[neighbour] = tentative_g_score
            came_from[neighbour] = (cell.x, cell.y)
            h_score = manhattan_distance(
                neighbour[0], exit[0], neighbour[1], exit[1]
            )
            f_score = h_score + g_score[neighbour]
            heappush(frontier, (f_score, counter(), neighbour))


def compile_path(
    entry: tuple[int, int],
    came_from: dict[tuple[int, int], tuple[int, int]],
    exit: tuple[int, int],
) -> str:
    """Build a string describing the path from the entry to the exit.

    Args:
        entry: Coordinates of the maze entry.
        came_from: Dictionary mapping each cell to the previous cell
            in the path.
        exit: Coordinates of the maze exit.

    Returns:
        A string of directions using ``N``, ``E``, ``S``, and ``W``.
    """

    current = exit
    path: list[str] = []
    while current != entry:
        previous_cell = came_from[current]
        if previous_cell[0] < current[0]:
            path.append("E")
        elif previous_cell[0] > current[0]:
            path.append("W")
        elif previous_cell[1] < current[1]:
            path.append("S")
        elif previous_cell[1] > current[1]:
            path.append("N")
        current = previous_cell
    path.reverse()
    return "".join(path)


def find_path(
    exit: tuple[int, int], entry: tuple[int, int], grid: list[list[Cell]]
) -> str:
    """Find a path from the maze entry to the exit using A* search.

    Args:
        exit: Coordinates of the maze exit.
        entry: Coordinates of the maze entry.
        grid: Two-dimensional list containing the maze cells.

    Returns:
        A string of directions describing the path from the entry to
        the exit.
    """

    frontier: list[tuple[int, int, tuple[int, int]]] = []
    g_score = {entry: 0}
    counter = maze_counter()
    came_from: dict[tuple[int, int], tuple[int, int]] = {}
    heappush(frontier, (0, counter(), entry))
    while frontier:
        _, _, current_cell = heappop(frontier)
        if current_cell == exit:
            break
        update_neighbours(
            grid[current_cell[1]][current_cell[0]],
            frontier,
            g_score,
            exit,
            counter,
            came_from,
        )
    return compile_path(entry, came_from, exit)
