from config import Config
from maze.models import Cell
from maze import find_path


def parse_path_to_coords(
        start_pos: tuple[int, int], path_str: str
) -> list[tuple[int, int]]:
    x, y = start_pos
    coords = []
    moves = {"N": (0, -1), "S": (0, 1), "E": (1, 0), "W": (-1, 0)}

    for move in path_str:
        if move in moves:
            dx, dy = moves[move]
            x += dx
            y += dy
            coords.append((x, y))
    return coords


# def get_solution_coords(
#         config: Config,
#         grid: list[list[Cell]]
# ) -> list[tuple[int, int]]:
#     entry_pos = (int(config.entry.y), int(config.entry.x))
#     exit_pos = (int(config.exit.y), int(config.exit.x))
#     solution_str = find_path(exit_pos, entry_pos, grid)
#     if solution_str:
#         start_pos = (int(config.entry.y), int(config.entry.x))
#         return parse_path_to_coords(start_pos, solution_str)
#     return []


def get_solution_coords(
        config: Config,
        solution_str: str
) -> list[tuple[int, int]]:
    if solution_str:
        start_pos = (int(config.entry.y), int(config.entry.x))
        return parse_path_to_coords(start_pos, solution_str)
    return []