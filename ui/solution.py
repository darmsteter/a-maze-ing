from config.models import Config


def parse_path_to_coords(
    entry_pos: tuple[int, int], path_str: str
) -> list[tuple[int, int]]:
    """Convert a path string into a list of maze coordinates.

    Args:
        entry_pos: Coordinates of the maze entry.
        path_str: String of movement directions using ``N``, ``S``,
            ``E``, and ``W``.

    Returns:
        A list of coordinates reached by following the path.
    """

    x, y = entry_pos
    coords = []
    moves = {"N": (0, -1), "S": (0, 1), "E": (1, 0), "W": (-1, 0)}

    for move in path_str:
        if move in moves:
            dx, dy = moves[move]
            x += dx
            y += dy
            coords.append((x, y))
    return coords


def get_solution_coordinates(
    config: Config, solution_str: str
) -> list[tuple[int, int]]:
    """Get the maze coordinates corresponding to a solution path.

    Args:
        config: Maze configuration containing the entry coordinates.
        solution_str: String describing the solution path.

    Returns:
        A list of coordinates along the solution path. Returns an empty
        list if the solution path is empty.
    """

    if solution_str:
        entry_pos = (int(config.entry.x), int(config.entry.y))
        return parse_path_to_coords(entry_pos, solution_str)
    return []
