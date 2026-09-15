import time
from blessed import Terminal
from config import Config
from maze.models import Cell
from ui.controller_menu import check_terminal_size, draw_controller_menu
from ui.themes import get_tile


def draw_maze_frame_and_title(
        term: Terminal,
        width: int,
        height: int,
        title: str = "A_MAZE_ING GAME"
) -> None:
    title_x = max(0, (width - len(title)) // 2)
    print(term.move_xy(title_x, 0) + term.bold_cyan(title), flush=True)

    top_border = (
        term.bold("┌") + term.bold("─") * (width - 2) + term.bold("┐")
    )
    bottom_border = (
        term.bold("└") + term.bold("─") * (width - 2) + term.bold("┘")
    )

    print(term.move_xy(0, 1) + term.bold_dim_gray(top_border), flush=True)
    for y in range(2, height + 2):
        print(term.move_xy(0, y) + term.bold_dim_gray("|"), flush=True)
        print(term.move_xy(width - 1, y) + term.bold_dim_gray("|"), flush=True)
    print(term.move_xy(0, height + 2)
          + term.bold_dim_gray(bottom_border), flush=True)


def draw_solution_str(
        term: Terminal,
        path: list[tuple[int, int]],
        grid: list[list[Cell]],
        config: Config,
        theme_name: str,
        mode: str,
        animate: bool = False,
        delay: float = 0.05
):
    if not path:
        return

    sol_tile = get_tile(term, "solution_path", theme_name, mode=mode)
    start = int(config.entry.x), int(config.entry.y)
    full_path = [start] + path

    def draw_step(x: int, y: int) -> None:
        print(term.move_xy(x * 2, y) + sol_tile, flush=True)
        if animate:
            time.sleep(delay)

    for i in range(1, len(full_path)):
        prev_x, prev_y = full_path[i - 1]
        curr_x, curr_y = full_path[i]

        # Extended coordinates for the previous and current cell
        p_x, p_y = prev_x * 2 + 1, prev_y * 2 + 1
        c_x, c_y = curr_x * 2 + 1, curr_y * 2 + 1

        # We calculate the position of the broken wall.
        mid_x = (p_x + c_x) // 2
        mid_y = (p_y + c_y) // 2
        # We draw the intermediate corridor
        draw_step(mid_x, mid_y)

        # We draw the current cell (if we haven't reached the exit).
        if not grid[curr_y][curr_x].is_exit(config):
            draw_step(c_x, c_y)


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
        top_line = wall_tile
        mid_line = wall_tile

        for cell in row:
            top_wall = wall_tile if cell.top else path_tile
            top_line += top_wall + wall_tile

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

    bottom_line = wall_tile * (len(grid[0]) * 2 + 1)
    print(term.move_xy(0, len(grid) * 2) + bottom_line, flush=True)


def draw_maze_emojis(
        term: Terminal,
        display_grid: list[list[str]],
        theme_name: str
):
    """Randering the grill extinded by emojis"""
    for y, row in enumerate(display_grid):
        tile = ""
        for char in row:
            if char == 'W':
                tile += get_tile(term, "wall", theme_name, mode="emoji")
            elif char == '4':
                tile += get_tile(term, "pattern_42", theme_name, mode="emoji")
            elif char == 'S':
                tile += get_tile(term, "start", theme_name, mode="emoji")
            elif char == 'E':
                tile += get_tile(term, "exit", theme_name, mode="emoji")
            else:
                tile += get_tile(term, "path", theme_name, mode="emoji")

        print(term.move_xy(0, y) + tile, flush=True)


def render_all(
    term: Terminal,
    config: Config,
    grid: list[list[Cell]],
    theme_name: str,
    mode: str,
    show_solution: bool,
    solution_coords: list[tuple[int, int]],
    display_grid: list[list[str]],
    animate_path: bool = False
):
    if not check_terminal_size(term, mode, display_grid, grid):
        return

    # Clean the entire screen.
    print(term.home + term.clear, end="", flush=True)

    # First, we draw the maze.
    if mode == "emoji" and display_grid:
        draw_maze_emojis(term, display_grid, theme_name)
        max_y = len(display_grid)
    else:
        draw_maze_lines(term, grid, config, theme_name)
        max_y = len(grid) * 2

    draw_controller_menu(term, max_y, show_solution, theme_name, mode)
    if show_solution and solution_coords:
        draw_solution_str(
            term, solution_coords, grid, config, theme_name, mode=mode,
            animate=animate_path, delay=0.03
        )
