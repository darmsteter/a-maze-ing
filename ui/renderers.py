import textwrap
from blessed import Terminal
from config import Config
from maze.models import Cell
from ui.controller_menu import check_terminal_size, draw_controller_menu
from errors import ActionInterrupted
from ui.themes import get_tile


def get_maze_frame_and_title(
    term: Terminal,
    frame_w: int,
    frame_h: int,
    offset_x: int,
    offset_y: int,
    title: str = "A_MAZE_ING GAME"
) -> list[str]:
    buffer = []
    top_bdr = term.bold("╔") + term.bold("═") * (frame_w - 2) + term.bold("╗")
    buffer.append(term.move_xy(offset_x, offset_y) + term.bold_dim_green(top_bdr))

    title_x = offset_x + max(1, (frame_w - len(title)) // 2)
    buffer.append(term.move_xy(offset_x, offset_y + 1) + term.bold_dim_green("║"))
    buffer.append(term.move_xy(title_x, offset_y + 1) + term.bold_cyan(title))
    buffer.append(
        term.move_xy(offset_x + frame_w - 1, offset_y + 1) + term.bold_dim_green("║")
    )

    title_bdr = term.bold("╠") + term.bold("═") * (frame_w - 2) + term.bold("╣")
    buffer.append(term.move_xy(offset_x, offset_y + 2) + term.bold_dim_green(title_bdr))
    for y in range(3, frame_h - 3):
        buffer.append(term.move_xy(offset_x, offset_y + y) + term.bold_dim_green("║"))
        buffer.append(
            term.move_xy(offset_x + frame_w - 1, offset_y + y)
            + term.bold_dim_green("║")
        )

    menu_bdr = term.bold("╠") + term.bold("═") * (frame_w - 2) + term.bold("╣")
    buffer.append(
        term.move_xy(offset_x, offset_y + frame_h - 3) + term.bold_dim_green(menu_bdr)
    )
    buffer.append(
        term.move_xy(offset_x, offset_y + frame_h - 2) + term.bold_dim_green("║")
    )
    buffer.append(
        term.move_xy(offset_x + frame_w - 1, offset_y + frame_h - 2)
        + term.bold_dim_green("║")
    )

    bottom_bdr = term.bold("╚") + term.bold("═") * (frame_w - 2) + term.bold("╝")
    buffer.append(
        term.move_xy(offset_x, offset_y + frame_h - 1) + term.bold_dim_green(bottom_bdr)
    )

    return buffer


def render_frame(
    term: Terminal,
    config: Config,
    grid: list[list[Cell]],
    mode: str,
    display_grid: list[list[str]],
    title: str = "A_MAZE_ING GAME"
) -> tuple[list[str], int, int, int, int, int, int]:
    if (
        mode == "emoji"
        and display_grid
        and len(display_grid) > 0
        and len(display_grid[0]) > 0
    ):
        inner_w = len(display_grid[0]) * 2
        inner_h = len(display_grid)
    else:
        inner_w = (len(grid[0]) * 2 + 1) * 2 if grid else (config.width * 2 + 1) * 2
        inner_h = len(grid) * 2 + 1 if grid else config.height * 2 + 1

    frame_w = max(inner_w + 4, 99)
    frame_h = inner_h + 6

    offset_x = max(0, (term.width - frame_w) // 2)
    offset_y = max(0, (term.height - frame_h) // 2)

    buffer = get_maze_frame_and_title(
        term, frame_w, frame_h, offset_x, offset_y, title=title
    )

    maze_x = offset_x + (frame_w - inner_w) // 2
    maze_y = offset_y + 3

    return buffer, maze_x, maze_y, inner_h, frame_w, offset_x, offset_y


def get_maze_lines(
    term: Terminal,
    grid: list[list[Cell]],
    config: Config,
    theme_name: str,
    offset_x: int,
    offset_y: int
) -> list[str]:
    """
    Renders the classic grid using row-based themes with full outer bdrs.
    """
    wall_tile = get_tile(term, "wall", theme_name, mode="line")
    path_tile = get_tile(term, "path", theme_name, mode="line")
    pattern_42_tile = get_tile(term, "pattern_42", theme_name, mode="line")

    buffer = []

    for y, row in enumerate(grid):
        top_line = wall_tile
        mid_line = wall_tile

        for x, cell in enumerate(row):
            is_42 = getattr(cell, "is_42", False)
            top_is_42 = y > 0 and getattr(grid[y - 1][x], "is_42", False)
            right_is_42 = x < len(row) - 1 and getattr(grid[y][x + 1], "is_42", False)
            if is_42 and top_is_42:
                top_wall = pattern_42_tile
            else:
                top_wall = wall_tile if cell.top else path_tile

            # Cell and right wall
            if is_42:
                tile = pattern_42_tile
            elif cell.is_start(config):
                tile = get_tile(term, "start", theme_name, mode="line")
            elif cell.is_exit(config):
                tile = get_tile(term, "exit", theme_name, mode="line")
            else:
                tile = path_tile

            if is_42 and right_is_42:
                right_wall = pattern_42_tile
            else:
                right_wall = wall_tile if cell.right else path_tile

            top_line += top_wall + wall_tile
            mid_line += tile + right_wall

        buffer.append(term.move_xy(offset_x, offset_y + y * 2) + top_line)
        buffer.append(term.move_xy(offset_x, offset_y + y * 2 + 1) + mid_line)

    bottom_line = wall_tile * (len(grid[0]) * 2 + 1)
    buffer.append(term.move_xy(offset_x, offset_y + len(grid) * 2) + bottom_line)
    return buffer


def get_maze_emojis(
    term: Terminal,
    display_grid: list[list[str]],
    theme_name: str,
    offset_x: int,
    offset_y: int
) -> list[str]:
    """Randering the grill extinded by emojis"""

    pattern_42_tile = get_tile(term, "pattern_42", theme_name, mode="emoji")
    buffer = []

    for y, row in enumerate(display_grid):
        tile = ""
        for char in row:
            if char == "4":
                tile += pattern_42_tile
            elif char == "W":
                tile += get_tile(term, "wall", theme_name, mode="emoji")
            elif char == "S":
                tile += get_tile(term, "start", theme_name, mode="emoji")
            elif char == "E":
                tile += get_tile(term, "exit", theme_name, mode="emoji")
            else:
                tile += get_tile(term, "path", theme_name, mode="emoji")

        buffer.append(term.move_xy(offset_x, offset_y + y) + tile)
    return buffer


def get_solution_str(
    term: Terminal,
    path: list[tuple[int, int]],
    grid: list[list[Cell]],
    config: Config,
    theme_name: str,
    mode: str,
    offset_x: int = 0,
    offset_y: int = 0,
    animate: bool = False,
    delay: float = 0.05
):
    if not path:
        return

    sol_tile = get_tile(term, "solution_path", theme_name, mode=mode)
    start = int(config.entry.x), int(config.entry.y)
    full_path = [start] + path

    allowed_keys = {"a", "q", "r", "s", "t", "m", "KEY_RESIZE", "KEY_ESCAPE"}

    def get_step(x: int, y: int) -> None:
        print(term.move_xy(offset_x + x * 2, offset_y + y) + sol_tile, flush=True)
        if animate:
            key = term.inkey(timeout=delay)
            if key:
                key_code = key.name if key.is_sequence else key.lower()
                if key_code in allowed_keys:
                    raise ActionInterrupted(key_code)

    for i in range(1, len(full_path)):
        prev_x, prev_y = full_path[i - 1]
        curr_x, curr_y = full_path[i]

        # Extended coordinates for the previous and current cell
        p_x, p_y = prev_x * 2 + 1, prev_y * 2 + 1
        c_x, c_y = curr_x * 2 + 1, curr_y * 2 + 1

        # We calculate the position of the broken wall.
        mid_x = (p_x + c_x) // 2
        mid_y = (p_y + c_y) // 2
        # We get the intermediate corridor
        get_step(mid_x, mid_y)

        # We get the current cell (if we haven't reached the exit).
        if not grid[curr_y][curr_x].is_exit(config):
            get_step(c_x, c_y)


def get_error_popup(term: Terminal, error_msg: str) -> None:
    popup_w = 64
    popup_h = 9

    start_x = (term.width - popup_w) // 2
    start_y = (term.height - popup_h) // 2

    border_color = term.bold_white
    bg_color = term.on_red
    text_color = term.bold_darkblue

    buffer = [str(term.home) + str(term.clear)]

    for i in range(popup_h):
        buffer.append(term.move_xy(start_x, start_y + i) + bg_color(" " * popup_w))

    top_border = border_color("╔" + "═" * (popup_w - 2) + "╗")
    buffer.append(term.move_xy(start_x, start_y) + bg_color(top_border))

    for i in range(1, popup_h - 1):
        middle_line = border_color("║" + " " * (popup_w - 2))
        buffer.append(term.move_xy(start_x, start_y + i) + bg_color(middle_line))

    bottom_border = border_color("╚" + "═" * (popup_w - 2) + "╝")
    buffer.append(
        term.move_xy(start_x, start_y + popup_h - 1) + bg_color(bottom_border)
    )

    title_raw = " CONFIGURATION ERROR "
    title = f"{term.bold_white(title_raw)} "
    title_x = start_x + (popup_w - len(title_raw)) // 2
    buffer.append(term.move_xy(title_x, start_y) + title)

    clean_msg = term.strip_seqs(error_msg)
    wrapped_lines = textwrap.wrap(clean_msg, width=popup_w - 6)
    for idx, line in enumerate(wrapped_lines[:4]):
        line_x = start_x + (popup_w - len(line)) // 2
        buffer.append(
            term.move_xy(line_x, start_y + 2 + idx)
            + bg_color(text_color(line))
        )

    prompt_raw = " Adjust config.txt and regenerate [R] "
    prompt = term.bold_darkblue(prompt_raw)
    prompt_x = start_x + (popup_w - len(term.strip_seqs(prompt))) // 2
    buffer.append(term.move_xy(prompt_x, start_y + popup_h - 2)
                  + bg_color(prompt))

    print("".join(buffer), flush=True)


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

    main_buff: list[str] = [str(term.home)]

    frame_buff, maze_x, maze_y, inner_h, frame_w, offset_x, offset_y = render_frame(
        term, config, grid, mode, display_grid
    )
    main_buff.extend(frame_buff)
    if mode == "emoji":
        main_buff.extend(
            get_maze_emojis(
                term, display_grid, theme_name, offset_x=maze_x, offset_y=maze_y
            )
        )
    else:
        main_buff.extend(
            get_maze_lines(
                term, grid, config, theme_name, offset_x=maze_x, offset_y=maze_y
            )
        )
    print("".join(main_buff), flush=True)

    menu_y = offset_y + inner_h + 4
    draw_controller_menu(
        term,
        x=offset_x,
        y=menu_y,
        show_solution=show_solution,
        theme_name=theme_name,
        mode=mode,
        frame_w=frame_w,
    )
    if show_solution and solution_coords:
        get_solution_str(
            term,
            solution_coords,
            grid,
            config,
            theme_name,
            mode=mode,
            offset_x=maze_x,
            offset_y=maze_y,
            animate=animate_path,
            delay=0.03,
        )
