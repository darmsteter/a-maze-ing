from blessed import Terminal
from typing import Any
from config import Config
from config.parser import read_config_file
from errors import ActionInterrupted, ConfigurationException
from maze.models import Cell
from maze.generate_maze import MazeGenerator
from ui.controller_menu import handle_input
from .grid_converter import to_display_grid
from ui.renderers import render_all, get_error_popup
from ui.solution import get_solution_coords


def grafic_initialization(
    config: Config,
    grid: list[list[Cell]],
    display_grid: list[list[str]],
    initial_path: str = "",
    theme_name: str = "tree_garden",
    mode: str = "emoji",
    show_solution: bool = False,
    config_path: str = "config.txt"
):
    generate = MazeGenerator()
    term = Terminal()

    current_state: dict[str, Any] = {
        "config": config,
        "grid": grid,
        "display_grid": display_grid,
        "path": initial_path,
        "needs_clear": False
    }

    def step_callback(step_grid: list[list[Cell]]) -> None:
        if current_state.get("needs_clear", False):
            print(str(term.home) + str(term.clear), end="", flush=True)
            current_state["needs_clear"] = False
        
        active_config = current_state["config"]
        temp_display = to_display_grid(
            step_grid, active_config.width, active_config.height, active_config
        )
        current_theme = current_state.get("theme_name", theme_name)
        current_mode = current_state.get("mode", mode)
        render_all(
            term,
            active_config,
            step_grid,
            current_theme,
            current_mode,
            show_solution=False,
            solution_coords=[],
            display_grid=temp_display,
            animate_path=False
        )
        key = term.inkey(timeout=0.02)
        allowed_keys = {"a", "q", "r", "s", "t", "m", "KEY_RESIZE", "KEY_ESCAPE"}
        if key:
            key_code = key.name if key.is_sequence else key.lower()
            if key_code in allowed_keys:
                raise ActionInterrupted(key_code)

    def generate_run(
        active_config: Config, animate: bool = False, reuse_current: bool = False
    ) -> tuple[list[list[Cell]], Config, str]:
        while True:
            try:
                if reuse_current:
                    new_config = active_config
                else:
                    new_config = read_config_file(config_path)

                cb = step_callback if animate else None
                current_seed = active_config.seed if reuse_current else new_config.seed

                new_grid, new_path = generate.generate(
                    new_config.height,
                    new_config.width,
                    (new_config.entry.x, new_config.entry.y),
                    (new_config.exit.x, new_config.exit.y),
                    new_config.seed,
                    new_config.perfect,
                    new_config.algorithm,
                    callback=cb
                )
                break
            except ConfigurationException as e:
                current_state["needs_clear"] = True
                get_error_popup(term, str(e))
                while True:
                    key = term.inkey(timeout=0.1)
                    if not key:
                        continue
                    key_code = key.name if key.is_sequence else key.lower()
                    if key_code in ("q", "KEY_ESCAPE"):
                        raise SystemExit(0)
                    if key_code == "r":
                        print(str(term.home) + str(term.clear), end="", flush=True)
                        break

        new_display_grid = to_display_grid(
            new_grid, new_config.width, new_config.height, new_config
        )

        current_state["config"] = new_config
        current_state["grid"] = new_grid
        current_state["display_grid"] = new_display_grid
        current_state["path"] = new_path

        return new_grid, new_config, new_path

    def refresh_ui(
        curr_grid: list[list[Cell]],
        curr_disp: list[list[str]],
        curr_theme: str,
        curr_mode: str,
        curr_sol: bool,
        curr_path: str = "",
        animate: bool = False
    ) -> None:
        current_state["theme_name"] = curr_theme
        current_state["mode"] = curr_mode
        path_to_use = curr_path if curr_path else current_state["path"]

        solution_coords = (
            get_solution_coords(current_state["config"], path_to_use)
            if curr_sol
            else []
        )
        render_all(
            term,
            current_state["config"],
            curr_grid,
            curr_theme,
            curr_mode,
            curr_sol,
            solution_coords,
            curr_disp,
            animate_path=animate
        )

    with term.fullscreen(), term.raw(), term.hidden_cursor():
        refresh_ui(
            grid,
            display_grid,
            theme_name,
            mode,
            show_solution,
            curr_path=initial_path,
            animate=False
        )
        handle_input(
            term,
            current_state["config"],
            grid,
            display_grid,
            theme_name,
            mode,
            show_solution,
            generate_fn=generate_run,
            refresh_ui_fn=refresh_ui,
            to_display_grid_fn=to_display_grid,
            path=initial_path
        )
