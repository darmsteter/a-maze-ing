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
        inner_w = len(display_grid[0]) * 2
        inner_h = len(display_grid)
    else:
        grid_width = len(grid[0]) if grid else 0
        grid_height = len(grid) if grid else 0
        inner_w = (grid_width * 2 + 1) * 2
        inner_h = grid_height * 2 + 1

    required_w = max(inner_w + 4, 99)
    required_h = inner_h + 7
    if term.width < required_w or term.height < required_h:
        msg = term.red_on_yellow(
            "Enlarge the terminal to see the maze! Regenerate (R)"
        )
        print(term.home + term.clear, end="", flush=True)
        print(term.move_xy(
            max(0, (term.width - len(term.strip_seqs(msg))) // 2),
            term.height // 2) + msg, flush=True)
        # print(term.center(msg))
        return False
    return True


def draw_controller_menu(
    term: Terminal,
    x: int,
    y: int,
    show_solution: bool,
    theme_name: str,
    mode: str,
    frame_w: int = 0,
):
    sol_status = term.green("ON") if show_solution else term.red("OFF")
    controls_menu = (
        f" {term.bold_yellow('[R]')} Reg: | "
        f"{term.bold_yellow('[S]')} Sol: {sol_status} | "
        f"{term.bold_yellow('[T]')} Theme: {term.yellow(theme_name)} | "
        f"{term.bold_orange('[M]')} Mode: {term.magenta(mode)} | "
        f"{term.bold_pink('[A]')} Live Gen | "
        f"{term.bold_red('[Q/ESC]')} Exit"
    )
    if frame_w > 0:
        visible_len = len(term.strip_seqs(controls_menu))
        draw_x = x + max(1, (frame_w - visible_len) // 2)
    else:
        draw_x = x

    print(f"{term.move_xy(draw_x, y)} {controls_menu}", flush=True)


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
    to_display_grid_fn,
    path: str = ""
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
                    mode, show_solution, curr_path=path, animate=False
                )
            elif key_code == 'r':
                grid, config, path = generate_fn(config)
                if mode == "emoji":
                    display_grid = to_display_grid_fn(
                        grid, config.width, config.height, config
                    )
                show_solution = False
                refresh_ui_fn(
                    grid, display_grid, theme_name,
                    mode, show_solution, curr_path=path, animate=False
                )
            elif key_code == 's':
                show_solution = not show_solution
                refresh_ui_fn(
                    grid, display_grid, theme_name,
                    mode, show_solution, curr_path=path, animate=show_solution
                )
            elif key_code == 't':
                theme_index = (theme_index + 1) % len(available_themes)
                theme_name = available_themes[theme_index]
                refresh_ui_fn(
                    grid, display_grid, theme_name,
                    mode, show_solution, curr_path=path, animate=False
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
                    mode, show_solution, curr_path=path, animate=False
                )
            elif key_code == 'a':
                grid, config, path = generate_fn(config, animate=True)
                if mode == "emoji":
                    display_grid = to_display_grid_fn(
                        grid, config.width, config.height, config
                    )
                show_solution = False
                refresh_ui_fn(
                    grid, display_grid, theme_name,
                    mode, show_solution, curr_path=path, animate=False
                )
        except KeyboardInterrupt:
            pass
