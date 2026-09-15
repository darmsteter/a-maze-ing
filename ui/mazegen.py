from blessed import Terminal
from config import Config
from maze.models import Cell
from maze.generate_maze import generate_maze
from .grid_converter import to_display_grid
from ui.renderers import render_all
from .themes import EMOJI_THEMES, LINE_THEMES
from solution import get_solution_coords


def grafic_initialization(
        config: Config,
        grid: list[list[Cell]],
        display_grid: list[list[str]] = None,
        theme_name: str = "tree_garden",
        mode: str = "emoji",
        show_solution: bool = False
):
    term = Terminal()
    available_themes = list(
        EMOJI_THEMES.keys())if mode == "emoji" else list(LINE_THEMES)
    theme_index = available_themes.index(
        theme_name) if theme_name in available_themes else 0

    def refresh_ui(animate: bool = False) -> None:
        solution_coords = get_solution_coords(
            config, grid) if show_solution else []
        render_all(
            term, config, grid, theme_name, mode,
            show_solution, solution_coords, display_grid, animate_path=animate
        )

    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        refresh_ui(animate=False)
        while True:
            key = term.inkey(timeout=0.1)

            if key.code == term.KEY_ESCAPE or key.lower() == 'q':
                break

            if key.is_sequence and key.name == "KEY_RESIZE":
                refresh_ui(animate=False)
            elif key.lower() == 'r':
                grid, path = generate_maze(config)
                if mode == "emoji":
                    display_grid = to_display_grid(
                        grid,
                        config.width,
                        config.height,
                        config
                    )
                show_solution = False
                refresh_ui(animate=False)

            elif key.lower() == 's':
                show_solution = not show_solution
                refresh_ui(animate=show_solution)
                # else:
                #     solution_coords = []
                #     render_all(animate_path=False)
                # render_all(animate_path=True)

            elif key.lower() == 't':
                theme_index = (theme_index + 1) % len(available_themes)
                theme_name = available_themes[theme_index]
                refresh_ui(animate=False)

            elif key.lower() == 'm':
                mode = "line" if mode == "emoji" else "emoji"
                available_themes = list(EMOJI_THEMES.keys(
                )) if mode == "emoji" else list(LINE_THEMES.keys())

                theme_index = 0
                theme_name = available_themes[0]

                if mode == "emoji" and not display_grid:
                    display_grid = to_display_grid(
                        grid, config.width, config.height, config
                    )
                refresh_ui(animate=False)

