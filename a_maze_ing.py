import sys
from config import read_config_file
from errors import ConfigurationException
from ui.grid_converter import to_display_grid
from ui import grafic_initialization
from maze.generate_maze import MazeGenerator


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(
            "Your program must be run with the following command: "
            "python3 a_maze_ing.py file_name.txt"
        )
        exit()
    try:
        config = read_config_file(sys.argv[1])
        generator = MazeGenerator()
        grid, path = generator.generate(
            config.height,
            config.width,
            (config.entry.y, config.entry.x),
            (config.exit.y, config.exit.x),
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
    except ConfigurationException as e:
        print(f"Configuration error: {e}")
        exit()


# tree -I '__pycache__|.mypy_cache|env|.git' --> to tree ignore 