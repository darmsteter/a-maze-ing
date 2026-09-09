import sys
from config import read_config_file
from errors import ConfigurationException
from generator import to_display_grid
from mazegen import grafic_initialization
from maze.generate_maze import MazeGenerator


# if __name__ == "__main__":
#     try:
#         config = read_config_file(sys.argv[1])
#         grid, = generate_maze(config)
#         display_grid = to_display_grid(grid, config.width, config.height)
#         grafic_initialization(config, grid, display_grid, theme_name="tree_garden", mode="emoji")

#         # generate_output_file(grid, config, path)
#     except ConfigurationException as e:
#         print(f"Configuration error: {e}")
#         exit()


if __name__ == "__main__":
    try:
        config = read_config_file(sys.argv[1])
        generator = MazeGenerator()
        grid, path = generator.generate(
            config.height, 
            config.width, 
            (config.entry.x, config.entry.y), 
            (config.exit.x, config.exit.y), 
            config.seed, 
            config.perfect, 
            config.algorithm)
        display_grid = to_display_grid(grid, config.width, config.height)
        grafic_initialization(config, grid, display_grid, theme_name="tree_garden", mode="emoji")

        # generate_output_file(grid, config, path)
    except ConfigurationException as e:
        print(f"Configuration error: {e}")
        exit()
