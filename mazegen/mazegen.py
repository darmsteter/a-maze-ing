from blessed import Terminal
from config import Config
from maze import find_path
from maze.models import Cell
from .themes import EMOJI_THEMES, LINE_THEMES


def get_tile(
    term: Terminal,
    tile_type: str,
    theme_name: str = "tree_garden",
    mode: str = "emoji"
) -> str:
    """Getting the grafic format from selected theme"""
    themes_dict = EMOJI_THEMES if mode == "emoji" else LINE_THEMES
    default_theme = "tree_garden" if mode == "emoji" else "classic_pink"

    theme = themes_dict.get(theme_name, themes_dict[default_theme])
    tile_formatter = theme.get(tile_type, lambda t: '  ')

    return tile_formatter(term)


def draw_maze_emojis(
        term: Terminal,
        display_grid: list[list[str]],
        theme_name: str
):
    """Randering the grill extinded by emojis"""
    for y, row in enumerate(display_grid):
        line = ""
        for char in row:
            if char == 'W':
                line += get_tile(term, "wall", theme_name, mode="emoji")
            elif char == 'S':
                line += get_tile(term, "start", theme_name, mode="emoji")
            elif char == 'E':
                line += get_tile(term, "exit", theme_name, mode="emoji")
            else:
                line += get_tile(term, "path", theme_name, mode="emoji")

        print(term.move_xy(0, y) + line, flush=True)


"""de rezolvat problema bordurilor"""


def draw_maze_lines(
        term: Terminal,
        grid: list[list[Cell]],
        config: Config,
        theme_name: str
):
    """Renders the classic grid using row-based themes."""
    for  y, row in enumerate(grid):
        top_line = ""
        mid_line = ""

        for cell in row:
            # Top wall
            wall_tile = get_tile(term, "wall", theme_name, mode="line")
            path_tile = get_tile(term, "path", theme_name, mode="line")

            top_line += wall_tile if cell.top else path_tile

            # Cell and right wall
            if cell.is_start(config):
                tile = get_tile(term, "start", theme_name, mode="line")
            elif cell.is_exit(config):
                tile = get_tile(term, "exit", theme_name, mode="line")
            else:
                tile = path_tile

            right_wall = wall_tile if cell.right else path_tile
            mid_line += tile + right_wall

            print(term.move_xy(0, y * 2) + top_line, flush=True)
            print(term.move_xy(0, y * 2 + 1) + mid_line, flush=True)


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


# def draw_maze(term: Terminal, grid: list[list[Cell]], config: Config):
#     for y, row in enumerate(grid):
#         line_str = "".join(get_tile(term, cell, config) for cell in row)
#         print(term.move_xy(0, y) + line_str, flush=True)


# def draw_maze(term: Terminal, grid: list[list[Cell]], config: Config):
#     for y, row in enumerate(grid):
#         top_line = ""
#         mid_line = ""

#         for x, cell in enumerate(row):
#             top_line += '🌳' if cell.top else '🟫'

#             if cell.is_start(config):
#                 tile = '🌳'
#             elif cell.is_exit(config):
#                 tile = '🚪'
#             else:
#                 tile = '🟫'
#             right_wall = '🌳' if cell.right else '🟫'
#             mid_line += tile + right_wall
#         print(term.move_xy(0, y * 2) + top_line, flush=True)
#         print(term.move_xy(0, y * 2 + 1) + mid_line, flush=True)


def draw_solution_str(
        term: Terminal, path, grid: list[list[Cell]], config: Config
):
    for x, y in path:
        cell = grid[y][x]
        if cell.is_start(config) or cell.is_exit(config):
            continue
        print(term.move_xy(x * 2, y) + term.on_pink('🐾'), flush=True)


def grafic_initialization(
        config: Config,
        grid: list[list[Cell]],
        display_grid: list[list[str]] = None,
        theme_name: str = "tree_garden",
        mode: str = "emoji",
        show_solution: bool = True
):
    term = Terminal()

    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        print(term.home + term.clear, end="", flush=True)
        # Rendering by mode
        if mode == "emoji" and display_grid:
            draw_maze_emojis(term, display_grid, theme_name)
            max_y = len(display_grid)
        else:
            draw_maze_lines(term, grid, config, theme_name)
            max_y = len(grid) * 2

        if show_solution:
            solution_str = find_path(config, grid)
            if solution_str:
                start_pos = (int(config.entry.x), int(config.entry.y))
                solution_coords = parse_path_to_coords(start_pos, solution_str)
                draw_solution_str(term, solution_coords, grid, config)

        print(
            term.move_xy(0, max_y + 1)
            + term.bold("Press 'ESC' or 'q' to exit game!"),
            flush=True
        )
        # solution_str = find_path(config, grid)
        # if solution_str:
        #     start_pos = (config.entry.x, config.entry.y)
        #     solution_coords = parse_path_to_coords(start_pos, solution_str)
        #     draw_solution_str(term, solution_coords, grid, config)

        while True:
            key = term.inkey(timeout=0.1)

            if key.code == term.KEY_ESCAPE or key.lower() == 'q':
                break
