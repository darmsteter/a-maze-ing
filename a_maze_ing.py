import sys
from blessed import Terminal
from config import read_config_file
from errors import ConfigurationException, ConfigurationFileError
from maze.generate_maze import MazeGenerator
from maze.output_file import generate_output_file
from ui import get_error_popup, initialize_graphics, to_display_grid

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(
            "Your program must be run with the following command: "
            "python3 a_maze_ing.py file_name.txt"
        )
        exit()

    config_file = sys.argv[1]
    term = Terminal()

    with term.fullscreen(), term.raw(), term.hidden_cursor():
        while True:
            try:
                config = read_config_file(config_file)
                generator = MazeGenerator()
                grid, path = generator.generate(
                    config.height,
                    config.width,
                    (config.entry.x, config.entry.y),
                    (config.exit.x, config.exit.y),
                    config.seed,
                    config.perfect,
                    str(config.algorithm),
                )
                break
            except (ConfigurationFileError, ConfigurationException) as e:
                print(f"Configuration error: {e}")
                if isinstance(e, ConfigurationFileError):
                    error_msg = (
                        "Please make sure that config.txt exists "
                        "and has the correct name, then restart the program. "
                        f"Details: {e}. "
                    )
                    prompt = " Press [Q] or [Esc] to exit "
                else:
                    error_msg = str(e)
                    prompt = (
                        "Adjust config.txt and press [R]-> Regenerate"
                        "or [Q|Esc]-> Exit."
                    )
                get_error_popup(term, error_msg, prompt)
                while True:
                    key = term.inkey(timeout=0.1)
                    if not key:
                        continue
                    action_key = key.name if key.is_sequence else key.lower()
                    if action_key in ("q", "KEY_ESCAPE"):
                        print(
                            str(term.home) + str(term.clear),
                            end="",
                            flush=True,
                        )
                        print(
                            term.normal + term.show_cursor, end="", flush=True
                        )
                        raise SystemExit(0)
                    if action_key == "r":
                        print(
                            str(term.home) + str(term.clear),
                            end="",
                            flush=True,
                        )
                        break
    generate_output_file(grid, config, path)
    display_grid = to_display_grid(grid, config.width, config.height, config)
    initialize_graphics(
        config,
        grid,
        display_grid,
        initial_path=path,
        theme_name="tree_garden",
        mode="emoji",
    )
