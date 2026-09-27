from blessed import Terminal
from typing import Callable
from config.models import Config
from errors import ActionInterrupted, ConfigurationException
from maze.models import Cell
from ui.themes import EMOJI_THEMES, LINE_THEMES

GenerateFn = Callable[
    [Config, bool, bool], tuple[list[list[Cell]], Config, str]
]

RefreshUiFn = Callable[
    [list[list[Cell]], list[list[str]], str, str, bool, str, bool], None
]

ToDisplayGridFn = Callable[
    [list[list[Cell]], int, int, Config], list[list[str]]
]


def check_terminal_size(
    term: Terminal,
    mode: str,
    display_grid: list[list[str]],
    grid: list[list[Cell]],
) -> bool:
    if mode == "emoji" and display_grid:
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
        msg = term.blink_red3_on_lightgoldenrod1(
            "Enlarge the terminal to see the maze! Regenerate (R)"
        )
        print(term.home + term.clear, end="", flush=True)
        print(
            term.move_xy(
                max(0, (term.width - len(term.strip_seqs(msg))) // 2),
                term.height // 2,
            )
            + msg,
            flush=True,
        )
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
) -> None:
    sol_status = (
        term.bold_springgreen("ON") if show_solution else term.bold_red3("OFF")
    )
    controls_menu = (
        f"{term.bold_crimson('[R]')} Reg: | "
        f"{term.bold_crimson('[S]')} Sol: {term.bold(sol_status)} | "
        f"{term.bold_crimson('[T]')} Theme:"
        f"{term.bold_darkgoldenrod1(theme_name)} | "
        f"{term.bold_orangered('[M]')} Mode: {term.magenta(mode)} | "
        f"{term.bold_maroon('[A]')} Live Gen | "
        f"{term.bold_red3('[Q/ESC]')} EXIT"
    )
    visible_len = len(term.strip_seqs(controls_menu))

    if frame_w > 0:
        draw_x = x + max(1, (frame_w - visible_len) // 2)
    else:
        draw_x = x

    print(f"{term.move_xy(x, y)}{' ' * max(
        frame_w, visible_len)}", end="", flush=True)
    print(f"{term.move_xy(draw_x, y)}{controls_menu}", flush=True)


def handle_input(
    term: Terminal,
    config: Config,
    grid: list[list[Cell]],
    display_grid: list[list[str]],
    theme_name: str,
    mode: str,
    show_solution: bool,
    generate_fn: GenerateFn,
    refresh_ui_fn: RefreshUiFn,
    to_display_grid_fn: ToDisplayGridFn,
    path: str = "",
) -> None:
    from ui.renderers import get_error_popup

    ALLOWED_KEYS = {"a", "q", "r", "s", "t", "m", "KEY_RESIZE", "KEY_ESCAPE"}
    available_themes = (
        list(EMOJI_THEMES.keys())
        if mode == "emoji"
        else list(LINE_THEMES.keys())
    )
    theme_index = (
        available_themes.index(theme_name)
        if theme_name in available_themes
        else 0
    )
    next_key: str = ""

    while True:
        try:
            if next_key:
                key_code = next_key
                next_key = ""
            else:
                key = term.inkey(timeout=0.1)
                if not key:
                    continue
                key_name = key.name if key.is_sequence else None
                key_code = key_name if key_name is not None else key.lower()
            if key_code not in ALLOWED_KEYS:
                continue

            if key_code == "KEY_ESCAPE" or key_code == "q":
                break

            elif key_code == "KEY_RESIZE":
                refresh_ui_fn(
                    grid,
                    display_grid,
                    theme_name,
                    mode,
                    show_solution,
                    path,
                    False,
                )
            elif key_code == "r":
                print(str(term.home) + str(term.clear), end="", flush=True)
                try:
                    grid, config, path = generate_fn(config, False, False)
                    if mode == "emoji":
                        display_grid = to_display_grid_fn(
                            grid, config.width, config.height, config
                        )
                    show_solution = False
                    refresh_ui_fn(
                        grid,
                        display_grid,
                        theme_name,
                        mode,
                        show_solution,
                        path,
                        False,
                    )
                except ConfigurationException as e:
                    get_error_popup(term, str(e))
            elif key_code == "s":
                show_solution = not show_solution
                refresh_ui_fn(
                    grid,
                    display_grid,
                    theme_name,
                    mode,
                    show_solution,
                    path,
                    True,
                )
            elif key_code == "t":
                theme_index = (theme_index + 1) % len(available_themes)
                theme_name = available_themes[theme_index]
                refresh_ui_fn(
                    grid,
                    display_grid,
                    theme_name,
                    mode,
                    show_solution,
                    path,
                    False,
                )
            elif key_code == "m":
                mode = "line" if mode == "emoji" else "emoji"
                available_themes = (
                    list(EMOJI_THEMES.keys())
                    if mode == "emoji"
                    else list(LINE_THEMES.keys())
                )

                theme_index = 0
                theme_name = available_themes[theme_index]

                if mode == "emoji":
                    display_grid = to_display_grid_fn(
                        grid, config.width, config.height, config
                    )
                refresh_ui_fn(
                    grid,
                    display_grid,
                    theme_name,
                    mode,
                    show_solution,
                    path,
                    False,
                )
            elif key_code == "a":
                grid, config, path = generate_fn(config, True, True)
                if mode == "emoji":
                    display_grid = to_display_grid_fn(
                        grid, config.width, config.height, config
                    )
                show_solution = False
                refresh_ui_fn(
                    grid,
                    display_grid,
                    theme_name,
                    mode,
                    show_solution,
                    path,
                    False,
                )
        except ActionInterrupted as e:
            next_key = e.key_code
