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
        content_width = len(display_grid[0]) * 2
        content_height = len(display_grid)
    else:
        grid_width = len(grid[0]) if grid else 0
        grid_height = len(grid) if grid else 0
        content_width = (grid_width * 2 + 1) * 2
        content_height = grid_height * 2 + 1

    min_term_width = max(content_width + 4, 99)
    min_term_height = content_height + 7

    if term.width < min_term_width or term.height < min_term_height:
        warning_msg = term.blink_red3_on_lightgoldenrod1(
            "Enlarge the terminal to see the maze! Regenerate (R)"
        )
        msg_length = len(term.strip_seqs(warning_msg))
        centered_x = max(0, (term.width - msg_length)) // 2
        centered_y = term.height // 2
        print(term.home + term.clear, end="", flush=True)
        print(
            term.move_xy(centered_x, centered_y) + warning_msg,
            flush=True,
        )
        return False
    return True


def draw_controller_menu(
    term: Terminal,
    start_x: int,
    start_y: int,
    show_solution: bool,
    theme_name: str,
    mode: str,
    frame_width: int = 0,
) -> None:
    menu_bg_style = term.on_gray10
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
    menu_text_len = len(term.strip_seqs(controls_menu))
    content_width = frame_width - 2 if frame_width > 0 else menu_text_len

    padding_left = max(0, (content_width - menu_text_len) // 2)
    padding_right = max(0, content_width - menu_text_len - padding_left)

    menu_row = (
        menu_bg_style(" " * padding_left)
        + menu_bg_style(controls_menu)
        + menu_bg_style(" " * padding_right)
    )

    print(
        f"{term.move_xy(start_x + 1, start_y)}{menu_row}", end="", flush=True
    )


def handle_input(
    term: Terminal,
    config: Config,
    grid: list[list[Cell]],
    display_grid: list[list[str]],
    theme_name: str,
    mode: str,
    show_solution: bool,
    generate_fn: GenerateFn,
    refresh_ui_view_fn: RefreshUiFn,
    to_display_grid_fn: ToDisplayGridFn,
    path: str = "",
) -> None:
    from ui.renderers import get_error_popup

    SUPPORTED_ACTION_KEYS = {
        "a",
        "q",
        "r",
        "s",
        "t",
        "m",
        "KEY_RESIZE",
        "KEY_ESCAPE",
    }
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
    queued_input_key: str = ""

    while True:
        try:
            if queued_input_key:
                action_key = queued_input_key
                queued_input_key = ""
            else:
                pressed_key = term.inkey(timeout=0.1)
                if not pressed_key:
                    continue
                if pressed_key.is_sequence and pressed_key.name is not None:
                    key_identifier = pressed_key.name
                else:
                    key_identifier = pressed_key.lower()
                action_key = key_identifier
            if action_key not in SUPPORTED_ACTION_KEYS:
                continue

            if action_key == "KEY_ESCAPE" or action_key == "q":
                break

            elif action_key == "KEY_RESIZE":
                refresh_ui_view_fn(
                    grid,
                    display_grid,
                    theme_name,
                    mode,
                    show_solution,
                    path,
                    False,
                )
            elif action_key == "r":
                print(str(term.home) + str(term.clear), end="", flush=True)
                try:
                    grid, config, path = generate_fn(config, False, False)
                    if mode == "emoji":
                        display_grid = to_display_grid_fn(
                            grid, config.width, config.height, config
                        )
                    show_solution = False
                    refresh_ui_view_fn(
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
            elif action_key == "s":
                show_solution = not show_solution
                refresh_ui_view_fn(
                    grid,
                    display_grid,
                    theme_name,
                    mode,
                    show_solution,
                    path,
                    True,
                )
            elif action_key == "t":
                theme_index = (theme_index + 1) % len(available_themes)
                theme_name = available_themes[theme_index]
                refresh_ui_view_fn(
                    grid,
                    display_grid,
                    theme_name,
                    mode,
                    show_solution,
                    path,
                    False,
                )
            elif action_key == "m":
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
                refresh_ui_view_fn(
                    grid,
                    display_grid,
                    theme_name,
                    mode,
                    show_solution,
                    path,
                    False,
                )
            elif action_key == "a":
                grid, config, path = generate_fn(config, True, True)
                if mode == "emoji":
                    display_grid = to_display_grid_fn(
                        grid, config.width, config.height, config
                    )
                show_solution = False
                refresh_ui_view_fn(
                    grid,
                    display_grid,
                    theme_name,
                    mode,
                    show_solution,
                    path,
                    False,
                )
        except ActionInterrupted as e:
            queued_input_key = e.key_code
