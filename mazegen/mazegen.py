import time
from blessed import Terminal
from config import Config
from maze import find_path
from maze.generate_maze import generate_maze
from generator import to_display_grid
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
            elif char == '4':
                line += get_tile(term, "pattern_42", theme_name, mode="emoji")
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
    """
    Renders the classic grid using row-based themes with full outer borders.
    """
    wall_tile = get_tile(term, "wall", theme_name, mode="line")
    path_tile = get_tile(term, "path", theme_name, mode="line")
    for y, row in enumerate(grid):
        top_line = ""
        mid_line = ""

        for cell in row:
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

        print(term.move_xy(0, y * 2) + top_line + wall_tile, flush=True)
        print(term.move_xy(0, y * 2 + 1) + mid_line, flush=True)
    bottom_line = wall_tile * (len(grid[0]) * 2 + 1)
    print(term.move_xy(0, len(grid) * 2) + bottom_line, flush=True)


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


def draw_solution_str(
        term: Terminal,
        path: list[tuple[int, int]],
        grid: list[list[Cell]],
        config: Config, mode:
        str = "emoji",
        animate: bool = False,
        delay: float = 0.05
):
    if not path:
        return

    start = int(config.entry.x), int(config.entry.y)
    full_path = [start] + path

    for i in range(1, len(full_path)):
        prev_x, prev_y = full_path[i - 1]
        curr_x, curr_y = full_path[i]

        if mode == "emoji":
            # Extended coordinates for the previous and current cell
            p_gx, p_gy = prev_x * 2 + 1, prev_y * 2 + 1
            c_gx, c_gy = curr_x * 2 + 1, curr_y * 2 + 1

            # We calculate the position of the broken wall.
            mid_gx = (p_gx + c_gx) // 2
            mid_gy = (p_gy + c_gy) // 2

            # We draw the intermediate corridor (unless it is the entrance itself).
            if not (prev_x == int(config.entry.x) and
                    prev_y == int(config.entry.y)):
                print(term.move_xy(mid_gx * 2, mid_gy) + '🐾',
                      flush=True)
                if animate:
                    time.sleep(delay)

            # We draw the current cell (if we haven't reached the exit).
            if not grid[curr_y][curr_x].is_exit(config):
                print(term.move_xy(c_gx * 2, c_gy) + '🐾',
                      flush=True)
                if animate:
                    time.sleep(delay)
        else:
            p_lx, p_ly = prev_x * 2 + 1, prev_y * 2 + 1
            c_lx, c_ly = curr_x * 2 + 1, curr_y * 2 + 1

            mid_lx = (p_lx + c_lx) // 2
            mid_ly = (p_ly + c_ly) // 2

            if not (prev_x == int(config.entry.x) and
                    prev_y == int(config.entry.y)):
                print(term.move_xy(mid_lx * 2, mid_ly) + '🐾',
                      flush=True)
                if animate:
                    time.sleep(delay)

            # We draw the current cell (if we haven't reached the exit).
            if not grid[curr_y][curr_x].is_exit(config):
                print(term.move_xy(c_lx * 2, c_ly) + '🐾',
                      flush=True)
                if animate:
                    time.sleep(delay)


def grafic_initialization(
        config: Config,
        grid: list[list[Cell]],
        display_grid: list[list[str]] = None,
        theme_name: str = "tree_garden",
        mode: str = "emoji",
        show_solution: bool = False
):
    term = Terminal()

    available_themes = list(
        EMOJI_THEMES.keys())if mode == "emoji" else list(LINE_THEMES)
    theme_index = available_themes.index(
        theme_name) if theme_name in available_themes else 0
    
    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        solution_coords: list[tuple[int, int]] = []

        def update_solution():
            nonlocal solution_coords
            solution_coords = []
            solution_str = find_path(config, grid)
            if show_solution:
                if solution_str:
                    start_pos = (int(config.entry.x), int(config.entry.y))
                    solution_coords = parse_path_to_coords(
                        start_pos, solution_str)
        update_solution()

        def render_all(animate_path: bool = False):
            nonlocal theme_name

            # Clean the entire screen.
            print(term.home + term.clear, end="", flush=True)

            # Cheching dimensions
            if mode == 'emoji' and display_grid:
                required_w = len(display_grid[0]) * 2
                required_h = len(display_grid) + 2
            else:
                required_w = len(display_grid[0]) * 2 + 1
                required_h = len(display_grid) + 2 + 3

            if term.width < required_w or term.height < required_h:
                msg = "Enlarge the terminal to see the maze!"
                print(term.move_xy(0, 0) + term.black_on_yellow(msg),
                      flush=True)
            print(term.home + term.clear, end="", flush=True)

            # First, we draw the maze.
            if mode == "emoji" and display_grid:
                draw_maze_emojis(term, display_grid, theme_name)
                max_y = len(display_grid)
            else:
                draw_maze_lines(term, grid, config, theme_name)
                max_y = len(grid) * 2

            # We draw the command MENU below the maze
            sol_status = term.green("ON") if show_solution else term.red("OFF")
            controls_menu = (
                f" {term.bold_cyan('[R]')} Regenerate: | "
                f"{term.bold_cyan('[S]')} Solution: {sol_status} | "
                f"{term.bold_cyan('[T]')} Theme: {term.yellow(theme_name)} | "
                f"{term.bold_cyan('[M]')} Mode: {term.magenta(mode)} | "
                f"{term.bold_red('[Q/ESC]')} End game"
            )
            print(f"{term.move_xy(0, max_y + 1)} {controls_menu}", flush=True)

            if show_solution and solution_coords:
                draw_solution_str(
                    term, solution_coords, grid, config, mode=mode,
                    animate=animate_path, delay=0.03
                )
        render_all(animate_path=False)

        # Keyboard commands --- de rezolvat problema
        while True:
            key = term.inkey(timeout=0.1)

            if key.is_sequence and key.name == "KEY_RESIZE":
                render_all(animate_path=False)
            elif key.lower() == 'r':
                grid, path = generate_maze(config)
                if mode == "emoji":
                    display_grid = to_display_grid(
                        grid,
                        config.width,
                        config.height
                    )
                show_solution = False
                update_solution()
                render_all(animate_path=show_solution)
            elif key.lower() == 's':
                show_solution = not show_solution
                if show_solution:
                    update_solution()
                    render_all(animate_path=True)
                else:
                    solution_coords = []
                    render_all(animate_path=False)
                # render_all(animate_path=True)
            elif key.lower() == 't':
                theme_index = (theme_index + 1) % len(available_themes)
                theme_name = available_themes[theme_index]
                render_all(animate_path=False)
            elif key.lower() == 'm':
                mode = "line" if mode == "emoji" else "emoji"
                available_themes = list(EMOJI_THEMES.keys(
                )) if mode == "emoji" else list(LINE_THEMES.keys())
                theme_index = 0
                theme_name = available_themes[0]
                render_all(animate_path=False)

            if key.code == term.KEY_ESCAPE or key.lower() == 'q':
                break
