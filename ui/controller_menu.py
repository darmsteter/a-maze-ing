from blessed import Terminal
from maze.models import Cell


def check_terminal_size(
        term: Terminal,
        mode: str,
        display_grid: list[list[str]],
        grid: list[list[Cell]]
) -> bool:
    """
    Checkint to make sure that the terminal is large enough for our maze
    """
    if mode == 'emoji' and display_grid:
        required_w = len(display_grid[0]) * 2
        required_h = len(display_grid) + 2
    else:
        grid_width = len(grid[0]) if grid else 0
        grid_height = len(grid) if grid else 0
        required_w = grid_width * 2 + 1
        required_h = grid_height + 2 + 5

    if term.width < required_w or term.height < required_h:
        msg = "Enlarge the terminal to see the maze!"
        print(term.home + term.clear, end="", flush=True)
        print(term.move_xy(0, 0) + term.black_on_yellow(msg), flush=True)
        return False
    return True


def draw_controller_menu(
    term: Terminal,
    max_y: int,
    show_solution: bool,
    theme_name: str,
    mode: str
):
    sol_status = term.green("ON") if show_solution else term.red("OFF")
    controls_menu = (
        f" {term.bold_cyan('[R]')} Regenerate: | "
        f"{term.bold_cyan('[S]')} Solution: {sol_status} | "
        f"{term.bold_cyan('[T]')} Theme: {term.yellow(theme_name)} | "
        f"{term.bold_cyan('[M]')} Mode: {term.magenta(mode)} | "
        f"{term.bold_red('[Q/ESC]')} End game"
    )
    print(f"{term.move_xy(0, max_y + 1)} {controls_menu}", flush=True)
