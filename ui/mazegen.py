from blessed import Terminal
from typing import Any
from config import Config
from config.parser import read_config_file
from maze.models import Cell
from maze.generate_maze import MazeGenerator
from ui.controller_menu import handle_input
from .grid_converter import to_display_grid
from ui.renderers import render_all
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
        "path": initial_path
    }

    def generate_run(
            active_config: Config) -> tuple[list[list[Cell]], Config, str]:
        try:
            new_config = read_config_file(config_path)
        except Exception:
            new_config = active_config  # -> pop up message

        new_grid, new_path = generate.generate(
            new_config.height,
            new_config.width,
            (new_config.entry.x, new_config.entry.y),
            (new_config.exit.x, new_config.exit.y),
            new_config.seed,
            new_config.perfect,
            new_config.algorithm
        )
        current_state["config"] = new_config
        current_state["grid"] = new_grid
        current_state["path"] = new_path

        return new_grid, new_config, new_path

    def refresh_ui(
            curr_grid: list[list[Cell]],
            curr_disp: list[list[str]],
            curr_theme: str,
            curr_mode: str,
            curr_sol: bool,
            curr_path: str = "",
            animate: bool = False,
    ) -> None:
        path_to_use = curr_path if curr_path else current_state["path"]

        solution_coords = (
            get_solution_coords(current_state["config"], path_to_use)
            if curr_sol else []
        )
        render_all(
            term, current_state["config"], curr_grid, curr_theme, curr_mode,
            curr_sol, solution_coords, curr_disp, animate_path=animate
        )

    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        refresh_ui(
            grid, display_grid, theme_name, mode, show_solution,
            curr_path=initial_path, animate=False
        )
        handle_input(
            term, current_state["config"], grid, display_grid, theme_name,
            mode, show_solution,
            generate_fn=generate_run,
            refresh_ui_fn=refresh_ui,
            to_display_grid_fn=to_display_grid,
            path=initial_path
        )
