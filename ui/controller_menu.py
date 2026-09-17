from blessed import Terminal
from config.models import Config
from maze.models import Cell
from ui.themes import EMOJI_THEMES, LINE_THEMES


def check_terminal_size(
        term: Terminal,
        mode: str,
        display_grid: list[list[str]],
        grid: list[list[Cell]]
) -> bool:
    """
    Ensuring that the terminal is large enough to accommodate our maze.
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
        msg = "Enlarge the terminal to see the maze! Regenerate (R)"
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


def handle_input(
    term: Terminal,
    config: Config,
    grid: list[list[Cell]],
    display_grid: list[list[str]],
    theme_name: str,
    mode: str,
    show_solution: bool,
    generate_fn,
    refresh_ui_fn,
    to_display_grid_fn
):
    available_themes = list(
        EMOJI_THEMES.keys())if mode == "emoji" else list(LINE_THEMES.keys())
    theme_index = available_themes.index(
            theme_name) if theme_name in available_themes else 0
    while True:
        try:
            key = term.inkey(timeout=0.1)
            if not key:
                continue

            key_code = key.name if key.is_sequence else key.lower()

            if key_code == 'KEY_ESCAPE' or key_code == 'q':
                break

            elif key_code == 'KEY_RESIZE':
                refresh_ui_fn(
                    grid, display_grid, theme_name,
                    mode, show_solution, animate=False
                    )
            elif key_code == 'r':
                grid, path = generate_fn(config)
                if mode == "emoji":
                    display_grid = to_display_grid_fn(
                        new_grid,
                        new_config.width,
                        new_config.height,
                        new_config
                    )
                show_solution = False
                refresh_ui_fn(
                    new_grid, display_grid, theme_name,
                    mode, show_solution, animate=False
                )

            elif key_code == 's':
                show_solution = not show_solution
                refresh_ui_fn(
                    grid, display_grid, theme_name,
                    mode, show_solution, animate=show_solution
                )

            elif key_code == 't':
                theme_index = (theme_index + 1) % len(available_themes)
                theme_name = available_themes[theme_index]
                refresh_ui_fn(
                    grid, display_grid, theme_name,
                    mode, show_solution, animate=False
                )

            elif key_code == 'm':
                mode = "line" if mode == "emoji" else "emoji"
                available_themes = list(EMOJI_THEMES.keys(
                )) if mode == "emoji" else list(LINE_THEMES.keys())

                theme_index = 0
                theme_name = available_themes[theme_index]

                if mode == "emoji":
                    display_grid = to_display_grid_fn(
                        grid, config.width, config.height, config
                    )
                refresh_ui_fn(
                    grid, display_grid, theme_name,
                    mode, show_solution, animate=False
                )
        except KeyboardInterrupt:
            pass
