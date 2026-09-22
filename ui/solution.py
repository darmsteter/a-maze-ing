from config import Config


def parse_path_to_coords(
        entry_pos: tuple[int, int], path_str: str
) -> list[tuple[int, int]]:
    x, y = entry_pos
    coords = []
    moves = {
        "N": (0, -1),
        "S": (0, 1),
        "E": (1, 0),
        "W": (-1, 0)
    }

    for move in path_str:
        if move in moves:
            dx, dy = moves[move]
            x += dx
            y += dy
            coords.append((x, y))
    return coords


def get_solution_coords(
        config: Config,
        solution_str: str
) -> list[tuple[int, int]]:
    if solution_str:
        entry_pos = (int(config.entry.x), int(config.entry.y))
        return parse_path_to_coords(entry_pos, solution_str)
    return []
