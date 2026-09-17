from blessed import Terminal
from config import Config
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
        theme_name: str = "tree_garden",
        mode: str = "emoji",
        show_solution: bool = False
):
    generate = MazeGenerator()
    term = Terminal()
    
    def refresh_ui(
            curr_grid: list[list[Cell]],
            curr_disp: list[list[str]],
            curr_theme: str,
            curr_mode: str,
            curr_sol: bool,
            animate: bool = False
    ) -> None:
        solution_coords = get_solution_coords(
            config, curr_grid) if curr_sol else []
        render_all(
            term, config, curr_grid, curr_theme, curr_mode,
            curr_sol, solution_coords, curr_disp, animate_path=animate
        )

    def generate_run(config):
        return generate.generate(
            config.height,
            config.width,
            (config.entry.x, config.entry.y),
            (config.exit.x, config.exit.y),
            config.seed,
            config.perfect,
            config.algorithm
        )

    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        refresh_ui(
            grid, display_grid, theme_name, mode, show_solution, animate=False
        )
        handle_input(
            term, config, grid, display_grid, theme_name, mode, show_solution,
            generate_fn=generate_run,
            refresh_ui_fn=refresh_ui,
            to_display_grid_fn=to_display_grid
        )
