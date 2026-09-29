import textwrap
from blessed import Terminal

from config.models import Config
from errors import ActionInterrupted
from maze.models import Cell
from ui.themes import get_rendered_line


def buid_maze_frame_and_title(
    term: Terminal,
    frame_width: int,
    frame_height: int,
    offset_x: int,
    offset_y: int,
    title: str = "A_MAZE_ING GAME",
) -> list[str]:
    """Build the frame and title for the maze display.

    Args:
        term: Blessed terminal instance used for styling and positioning.
        frame_width: Width of the frame.
        frame_height: Height of the frame.
        offset_x: Horizontal position of the frame.
        offset_y: Vertical position of the frame.
        title: Title displayed at the top of the frame.

    Returns:
        A list of formatted terminal strings representing the frame.
    """

    buffer: list[str] = []
    bg_style = term.on_gray10
    wall_style = term.bold_darkgreen

    top_border = (
        term.bold("╔") + term.bold("═") * (frame_width - 2) + term.bold("╗")
    )
    buffer.append(
        term.move_xy(offset_x, offset_y) + term.bold_darkgreen(top_border)
    )

    title_left_padding = max(1, (frame_width - 2 - len(title)) // 2)
    title_right_padding = max(
        0, frame_width - 2 - len(title) - title_left_padding
    )
    title_raw = (
        term.move_xy(offset_x, offset_y + 1)
        + wall_style("║")
        + bg_style(" " * title_left_padding)
        + bg_style(term.bold_turquoise1(title))
        + bg_style(" " * title_right_padding)
        + wall_style("║")
    )
    buffer.append(title_raw)
    title_divider_border = (
        term.bold("╠") + term.bold("═") * (frame_width - 2) + term.bold("╣")
    )
    buffer.append(
        term.move_xy(offset_x, offset_y + 2)
        + term.bold_darkgreen(title_divider_border)
    )
    for current_row_chars in range(3, frame_height - 3):
        buffer.append(
            term.move_xy(offset_x, offset_y + current_row_chars)
            + wall_style("║")
            + bg_style(" " * (frame_width - 2))
            + wall_style("║")
        )

    menu_divider_border = (
        term.bold("╠") + term.bold("═") * (frame_width - 2) + term.bold("╣")
    )
    buffer.append(
        term.move_xy(offset_x, offset_y + frame_height - 3)
        + wall_style(menu_divider_border)
    )
    buffer.append(
        term.move_xy(offset_x, offset_y + frame_height - 2)
        + wall_style("║")
        + bg_style(" " * (frame_width - 2))
        + wall_style("║")
    )

    bottom_border = (
        term.bold("╚") + term.bold("═") * (frame_width - 2) + term.bold("╝")
    )
    buffer.append(
        term.move_xy(offset_x, offset_y + frame_height - 1)
        + wall_style(bottom_border)
    )

    return buffer


def render_frame(
    term: Terminal,
    config: Config,
    grid: list[list[Cell]],
    mode: str,
    display_grid: list[list[str]],
    title: str = "A_MAZE_ING GAME",
) -> tuple[list[str], int, int, int, int, int, int]:
    """Calculate the maze frame dimensions and position.

    Args:
        term: Blessed terminal instance used to determine terminal size.
        config: Maze configuration containing maze dimensions.
        grid: Generated maze grid.
        mode: Current maze display mode.
        display_grid: Formatted grid used in emoji mode.
        title: Title displayed at the top of the frame.

    Returns:
        A tuple containing the frame buffer, maze start coordinates,
        content height, frame width, and frame offsets.
    """

    if (
        mode == "emoji"
        and display_grid
        and len(display_grid) > 0
        and len(display_grid[0]) > 0
    ):
        content_width = len(display_grid[0]) * 2
        content_height = len(display_grid)
    else:
        content_width = (
            (len(grid[0]) * 2 + 1) * 2 if grid else (config.width * 2 + 1) * 2
        )
        content_height = len(grid) * 2 + 1 if grid else config.height * 2 + 1

    frame_width = max(content_width + 4, 99)
    frame_height = content_height + 6

    offset_x = max(0, (term.width - frame_width) // 2)
    offset_y = max(0, (term.height - frame_height) // 2)

    buffer = buid_maze_frame_and_title(
        term, frame_width, frame_height, offset_x, offset_y, title=title
    )

    maze_start_x = offset_x + (frame_width - content_width) // 2
    maze_start_y = offset_y + 3

    return (
        buffer,
        maze_start_x,
        maze_start_y,
        content_height,
        frame_width,
        offset_x,
        offset_y,
    )


def build_line_maze_buffer(
    term: Terminal,
    grid: list[list[Cell]],
    config: Config,
    theme_name: str,
    offset_x: int,
    offset_y: int,
) -> list[str]:
    """Build the terminal buffer for line-based maze rendering.

    Args:
        term: Blessed terminal instance used for styling and positioning.
        grid: Generated maze grid.
        config: Maze configuration containing the entry and exit positions.
        theme_name: Name of the display theme.
        offset_x: Horizontal position where the maze starts.
        offset_y: Vertical position where the maze starts.

    Returns:
        A list of formatted terminal strings representing the maze.
    """

    wall_rendered_line = get_rendered_line(
        term, "wall", theme_name, mode="line"
    )
    path_rendered_line = get_rendered_line(
        term, "path", theme_name, mode="line"
    )
    pattern_42_rendered_line = get_rendered_line(
        term, "pattern_42", theme_name, mode="line"
    )

    buffer = []

    for cell_y, row_chars in enumerate(grid):
        top_line = wall_rendered_line
        mid_line = wall_rendered_line

        for cell_x, cell in enumerate(row_chars):
            is_42 = getattr(cell, "is_42", False)
            top_neighbor_is_42 = cell_y > 0 and getattr(
                grid[cell_y - 1][cell_x], "is_42", False
            )
            right_neighbor_is_42 = cell_x < len(row_chars) - 1 and getattr(
                grid[cell_y][cell_x + 1], "is_42", False
            )
            if is_42 and top_neighbor_is_42:
                top_wall = pattern_42_rendered_line
            else:
                top_wall = (
                    wall_rendered_line if cell.top else path_rendered_line
                )

            if is_42:
                rendered_line = pattern_42_rendered_line
            elif cell.is_start(config):
                rendered_line = get_rendered_line(
                    term, "start", theme_name, mode="line"
                )
            elif cell.is_exit(config):
                rendered_line = get_rendered_line(
                    term, "exit", theme_name, mode="line"
                )
            else:
                rendered_line = path_rendered_line

            if is_42 and right_neighbor_is_42:
                right_wall = pattern_42_rendered_line
            else:
                right_wall = (
                    wall_rendered_line if cell.right else path_rendered_line
                )

            top_line += top_wall + wall_rendered_line
            mid_line += rendered_line + right_wall

        buffer.append(term.move_xy(offset_x, offset_y + cell_y * 2) + top_line)
        buffer.append(
            term.move_xy(offset_x, offset_y + cell_y * 2 + 1) + mid_line
        )

    bottom_line = wall_rendered_line * (len(grid[0]) * 2 + 1)
    buffer.append(
        term.move_xy(offset_x, offset_y + len(grid) * 2) + bottom_line
    )
    return buffer


def build_emoji_maze_buffer(
    term: Terminal,
    display_grid: list[list[str]],
    theme_name: str,
    offset_x: int,
    offset_y: int,
) -> list[str]:
    """Build the terminal buffer for emoji-based maze rendering.

    Args:
        term: Blessed terminal instance used for styling and positioning.
        display_grid: Grid containing characters representing the maze.
        theme_name: Name of the display theme.
        offset_x: Horizontal position where the maze starts.
        offset_y: Vertical position where the maze starts.

    Returns:
        A list of formatted terminal strings representing the maze.
    """

    buffer = []

    for row, row_chars in enumerate(display_grid):
        rendered_line = ""
        for char in row_chars:
            if char == "4":
                rendered_line += get_rendered_line(
                    term, "pattern_42", theme_name, mode="emoji"
                )
            elif char == "W":
                rendered_line += get_rendered_line(
                    term, "wall", theme_name, mode="emoji"
                )
            elif char == "S":
                rendered_line += get_rendered_line(
                    term, "start", theme_name, mode="emoji"
                )
            elif char == "E":
                rendered_line += get_rendered_line(
                    term, "exit", theme_name, mode="emoji"
                )
            else:
                rendered_line += get_rendered_line(
                    term, "path", theme_name, mode="emoji"
                )

        buffer.append(term.move_xy(offset_x, offset_y + row) + rendered_line)

    return buffer


def render_solution_path(
    term: Terminal,
    path_coordinates: list[tuple[int, int]],
    grid: list[list[Cell]],
    config: Config,
    theme_name: str,
    mode: str,
    offset_x: int = 0,
    offset_y: int = 0,
    animate: bool = False,
    delay: float = 0.05,
) -> None:
    """Render the solution path from the maze entry to the exit.

    When animation is enabled, keyboard input can interrupt the rendering.

    Args:
        term: Blessed terminal instance used for rendering and input.
        path_coordinates: Coordinates of cells in the solution path.
        grid: Maze grid containing the path.
        config: Maze configuration containing the entry and exit positions.
        theme_name: Name of the display theme.
        mode: Current maze display mode.
        offset_x: Horizontal position where the maze starts.
        offset_y: Vertical position where the maze starts.
        animate: Whether to render the path step by step.
        delay: Delay between animation steps in seconds.

    Raises:
        ActionInterrupted: If the user presses a supported control key
            during animated rendering.
    """

    if not path_coordinates:
        return

    solution_tile = get_rendered_line(
        term, "solution_path", theme_name, mode=mode
    )
    start_coordinates = int(config.entry.x), int(config.entry.y)
    full_solution_path = [start_coordinates] + path_coordinates

    supported_action_keys = {
        "a",
        "q",
        "r",
        "s",
        "t",
        "m",
        "KEY_RESIZE",
        "KEY_ESCAPE",
    }

    def render_path_step(x: int, y: int) -> None:
        print(
            term.move_xy(offset_x + x * 2, offset_y + y) + solution_tile,
            flush=True,
        )
        if animate:
            pressed_key = term.inkey(timeout=delay)
            if pressed_key:
                if pressed_key.is_sequence and pressed_key.name is not None:
                    key_identifier = pressed_key.name
                else:
                    key_identifier = pressed_key.lower()

                if key_identifier in supported_action_keys:
                    raise ActionInterrupted(key_identifier)

    for path_index in range(1, len(full_solution_path)):
        previous_x, previous_y = full_solution_path[path_index - 1]
        current_x, current_y = full_solution_path[path_index]

        prev_render_x, prev_render_y = previous_x * 2 + 1, previous_y * 2 + 1
        curr_render_x, curr_render_y = current_x * 2 + 1, current_y * 2 + 1

        mid_x = (prev_render_x + curr_render_x) // 2
        mid_y = (prev_render_y + curr_render_y) // 2
        render_path_step(mid_x, mid_y)

        if not grid[current_y][current_x].is_exit(config):
            render_path_step(curr_render_x, curr_render_y)


def get_error_popup(
    term: Terminal,
    error_msg: str,
    prompt_text: str = (
        "Adjust config.txt and press [R]-> Regenerate or [Q|Esc]-> Exit."
    ),
) -> None:
    """Display a configuration error popup in the terminal.

    Args:
        term: Blessed terminal instance used for positioning and styling.
        error_msg: Error message to display.
        prompt_text: Instructions displayed below the error message.
    """

    popup_w = 64
    popup_h = 9

    start_x = (term.width - popup_w) // 2
    start_y = (term.height - popup_h) // 2

    border_color = term.bold_darkred
    bg_color = term.on_indianred2
    text_color = term.bold_gray100

    buffer = [str(term.home) + str(term.clear)]

    for row_index in range(popup_h):
        buffer.append(
            term.move_xy(start_x, start_y + row_index)
            + bg_color(" " * popup_w)
        )

    top_border = border_color("╔" + "═" * (popup_w - 2) + "╗")
    buffer.append(term.move_xy(start_x, start_y) + bg_color(top_border))

    for i in range(1, popup_h - 1):
        mid_line = border_color("║" + " " * (popup_w - 2)) + border_color("║")
        buffer.append(term.move_xy(start_x, start_y + i) + bg_color(mid_line))

    bottom_border = border_color("╚" + "═" * (popup_w - 2) + "╝")
    buffer.append(
        term.move_xy(start_x, start_y + popup_h - 1) + bg_color(bottom_border)
    )

    title_raw = " CONFIGURATION ERROR "
    title = term.blink_bold_black_on_indianred2(title_raw)
    title_left_padding = start_x + (popup_w - len(title_raw)) // 2
    buffer.append(term.move_xy(title_left_padding, start_y) + title)

    clean_msg = term.strip_seqs(error_msg)
    wrapped_lines = textwrap.wrap(clean_msg, width=popup_w - 6)
    for index_line, line_str in enumerate(wrapped_lines[:4]):
        line_x = start_x + (popup_w - len(line_str)) // 2
        buffer.append(
            term.move_xy(line_x, start_y + 2 + index_line)
            + bg_color(text_color(line_str))
        )

    formatted_prompt = term.bold_gray100(prompt_text)
    prompt_x = (
        start_x + (popup_w - len(term.strip_seqs(formatted_prompt))) // 2
    )
    buffer.append(
        term.move_xy(prompt_x, start_y + popup_h - 2)
        + bg_color(formatted_prompt)
    )

    print("".join(buffer), flush=True)


def render_all(
    term: Terminal,
    config: Config,
    grid: list[list[Cell]],
    theme_name: str,
    mode: str,
    show_solution: bool,
    solution_coordinates: list[tuple[int, int]],
    display_grid: list[list[str]],
    animate_path: bool = False,
) -> None:
    """Render the complete maze interface.

    This includes the maze frame, maze contents, controller menu,
    and optionally the solution path.

    Args:
        term: Blessed terminal instance used for rendering.
        config: Maze configuration containing maze dimensions and positions.
        grid: Generated maze grid.
        theme_name: Name of the display theme.
        mode: Current maze display mode.
        show_solution: Whether to display the solution path.
        solution_coordinates: Coordinates of cells in the solution path.
        display_grid: Formatted grid used in emoji mode.
        animate_path: Whether to animate the solution path.
    """
    
    from .controller_menu import check_terminal_size, draw_controller_menu

    if not check_terminal_size(term, mode, display_grid, grid):
        return

    main_buff: list[str] = [str(term.home)]
    (
        frame_buff,
        maze_start_x,
        maze_start_y,
        content_height,
        frame_width,
        offset_x,
        offset_y,
    ) = render_frame(term, config, grid, mode, display_grid)
    main_buff.extend(frame_buff)

    if mode == "emoji":
        main_buff.extend(
            build_emoji_maze_buffer(
                term,
                display_grid,
                theme_name,
                offset_x=maze_start_x,
                offset_y=maze_start_y,
            )
        )
    else:
        main_buff.extend(
            build_line_maze_buffer(
                term,
                grid,
                config,
                theme_name,
                offset_x=maze_start_x,
                offset_y=maze_start_y,
            )
        )
    print("".join(main_buff), flush=True)

    menu_y = offset_y + content_height + 4
    draw_controller_menu(
        term,
        offset_x,
        menu_y,
        show_solution=show_solution,
        theme_name=theme_name,
        mode=mode,
        frame_width=frame_width,
    )

    if show_solution and solution_coordinates:
        render_solution_path(
            term,
            solution_coordinates,
            grid,
            config,
            theme_name,
            mode=mode,
            offset_x=maze_start_x,
            offset_y=maze_start_y,
            animate=animate_path,
            delay=0.03,
        )
