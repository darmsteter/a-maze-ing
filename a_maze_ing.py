import sys
from blessed import Terminal
from config import read_config_file
from errors import ConfigurationException
from ui.grid_converter import to_display_grid
from ui import grafic_initialization
from maze.generate_maze import MazeGenerator
from ui.renderers import get_error_popup


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
                break
            except ConfigurationException as e:
                print(f"Configuration error: {e}")
                get_error_popup(term, str(e))
                while True:
                    key = term.inkey(timeout=0.1)
                    if not key:
                        continue
                    key_code = key.name if key.is_sequence else key.lower()
                    if key_code in ("q", "KEY_ESCAPE"):
                        print(str(term.home) + str(term.clear), end="", flush=True)
                        print(term.normal + term.show_cursor, end="", flush=True)
                        raise SystemExit(0)
                    if key_code == "r":
                        print(str(term.home) + str(term.clear), end="", flush=True)
                        break
                # exit()
    generator = MazeGenerator()
    grid, path = generator.generate(
        config.height,
        config.width,
        (config.entry.x, config.entry.y),
        (config.exit.x, config.exit.y),
        config.seed,
        config.perfect,
        config.algorithm
    )
    display_grid = to_display_grid(
        grid, config.width, config.height, config
    )
    grafic_initialization(
        config, grid, display_grid,
        initial_path=path, theme_name="tree_garden", mode="emoji"
    )


# tree -I '__pycache__|.mypy_cache|env|.git' --> to tree ignore
