from typing import Any
from blessed import Terminal

from config.models import Config
from config.parser import read_config_file
from errors import (
    ActionInterrupted,
    ConfigurationException,
    ConfigurationFileError,
)
from mazegen.models import Cell
from mazegen.generate_maze import MazeGenerator
from mazegen.errors import MazeGenerationError
from maze_utils.find_path import find_path
from maze_utils.output_file import generate_output_file

from ui.controller_menu import handle_input
from ui.grid_converter import to_display_grid
from ui.renderers import render_all, get_error_popup
from ui.solution import get_solution_coordinates


def initialize_graphics(
    config: Config,
    grid: list[list[Cell]],
    display_grid: list[list[str]],
    initial_path: str = "",
    theme_name: str = "tree_garden",
    mode: str = "emoji",
    show_solution: bool = False,
    config_path: str = "config.txt",
) -> None:
    """Initialize the terminal interface and run the maze session.

    Sets up the terminal, displays the initial maze, and handles
    user interaction for the current maze session.

    Args:
        config: Maze configuration used for the initial maze.
        grid: Generated maze grid.
        display_grid: Formatted grid used for display.
        initial_path: Path from the maze entry to the exit.
        theme_name: Name of the initial display theme.
        mode: Initial maze display mode.
        show_solution: Whether to display the solution initially.
        config_path: Path to the maze configuration file.
    """

    maze_generator = MazeGenerator()
    term = Terminal()

    session_state: dict[str, Any] = {
        "config": config,
        "grid": grid,
        "display_grid": display_grid,
        "path": initial_path,
        "needs_screen_clear": False,
    }

    def animation_step_callback(step_grid: list[list[Cell]]) -> None:
        """Update the display during animated maze generation.

        Args:
            step_grid: Current state of the maze grid during generation.

        Raises:
            ActionInterrupted: If the user presses a supported control key
                during maze generation.
        """

        if session_state.get("needs_screen_clear", False):
            print(str(term.home) + str(term.clear), end="", flush=True)
            session_state["needs_screen_clear"] = False
            session_state["frame_drawn"] = False

        active_config = session_state["config"]
        current_theme = session_state.get("theme_name", theme_name)
        current_mode = session_state.get("mode", mode)

        step_display_grid = (
            to_display_grid(
                step_grid,
                active_config.width,
                active_config.height,
                active_config,
            )
            if current_mode == "emoji"
            else []
        )

        drawn = render_all(
            term,
            active_config,
            step_grid,
            current_theme,
            current_mode,
            show_solution=False,
            solution_coordinates=[],
            display_grid=step_display_grid,
            animate_path=False,
            draw_frame=not session_state.get("frame_drawn", False),
        )
        session_state["frame_drawn"] = drawn

        pressed_key = term.inkey(timeout=0.01)
        supported_action_key = {
            "a",
            "q",
            "r",
            "s",
            "t",
            "m",
            "KEY_RESIZE",
            "KEY_ESCAPE",
        }
        if pressed_key:
            if pressed_key.is_sequence and pressed_key.name is not None:
                key_identifier = pressed_key.name
            else:
                key_identifier = pressed_key.lower()
            if key_identifier in supported_action_key:
                raise ActionInterrupted(key_identifier)

    def generate_and_save_maze(
        active_config: Config,
        animate: bool = False,
        reuse_currentent_config: bool = False,
    ) -> tuple[list[list[Cell]], Config, str]:
        """Generate a maze, save it to a file, and update the session state.

        Args:
            active_config: Current maze configuration.
            animate: Whether to display the maze generation animation.
            reuse_currentent_config: Whether to reuse the provided configuration
                instead of reading it from the configuration file.

        Returns:
            A tuple containing the generated maze grid, its configuration,
            and the path from the entry to the exit.

        Raises:
            SystemExit: If the user chooses to exit while an invalid
                configuration is being handled.
        """

        while True:
            try:
                if reuse_currentent_config:
                    new_config = active_config
                else:
                    new_config = read_config_file(config_path)

                callback_fn = animation_step_callback if animate else None

                new_grid = maze_generator.generate(
                    new_config.height,
                    new_config.width,
                    (new_config.entry.x, new_config.entry.y),
                    (new_config.exit.x, new_config.exit.y),
                    new_config.seed,
                    new_config.perfect,
                    str(new_config.algorithm),
                    callback=callback_fn,
                )
                new_path = find_path(
                    (new_config.exit.x, new_config.exit.y),
                    (new_config.entry.x, new_config.entry.y),
                    new_grid
                )
                generate_output_file(new_grid, new_config, new_path)
                break
            except (ConfigurationFileError, ConfigurationException, MazeGenerationError) as e:
                session_state["needs_screen_clear"] = True
                get_error_popup(term, str(e))
                while True:
                    pressed_key = term.inkey(timeout=0.1)
                    if not pressed_key:
                        continue
                    if (
                        pressed_key.is_sequence
                        and pressed_key.name is not None
                    ):
                        key_identifier = pressed_key.name
                    else:
                        key_identifier = pressed_key.lower()
                    if key_identifier in ("q", "KEY_ESCAPE"):
                        print(
                            str(term.home) + str(term.clear),
                            end="",
                            flush=True,
                        )
                        print(
                            term.normal + term.show_cursor, end="", flush=True
                        )
                        raise SystemExit(0)
                    if key_identifier == "r":
                        print(
                            str(term.home) + str(term.clear),
                            end="",
                            flush=True,
                        )
                        break

        new_display_grid = to_display_grid(
            new_grid, new_config.width, new_config.height, new_config
        )

        session_state["config"] = new_config
        session_state["grid"] = new_grid
        session_state["display_grid"] = new_display_grid
        session_state["path"] = new_path

        return new_grid, new_config, new_path

    def refresh_ui_view(
        current_grid: list[list[Cell]],
        current_display_grid: list[list[str]],
        current_theme: str,
        current_mode: str,
        should_show_solution: bool,
        current_path: str = "",
        animate: bool = False,
    ) -> None:
        """Refresh the maze interface using the current display settings.

        Args:
            current_grid: Current maze grid.
            current_display_grid: Formatted grid used for display.
            current_theme: Name of the current display theme.
            current_mode: Current maze display mode.
            should_show_solution: Whether to display the maze solution.
            current_path: Path from the maze entry to the exit.
            animate: Whether to animate the displayed solution path.
        """

        session_state["theme_name"] = current_theme
        session_state["mode"] = current_mode
        active_path = current_path if current_path else session_state["path"]

        solution_coordinates = (
            get_solution_coordinates(session_state["config"], active_path)
            if should_show_solution
            else []
        )
        render_all(
            term,
            session_state["config"],
            current_grid,
            current_theme,
            current_mode,
            should_show_solution,
            solution_coordinates,
            current_display_grid,
            animate_path=animate,
        )

    with term.fullscreen(), term.raw(), term.hidden_cursor():
        refresh_ui_view(
            grid,
            display_grid,
            theme_name,
            mode,
            show_solution,
            current_path=initial_path,
            animate=False,
        )
        handle_input(
            term,
            session_state["config"],
            grid,
            display_grid,
            theme_name,
            mode,
            show_solution,
            generate_fn=generate_and_save_maze,
            refresh_ui_view_fn=refresh_ui_view,
            to_display_grid_fn=to_display_grid,
            path=initial_path,
        )
