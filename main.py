from config import read_config_file, Config
from errors import ConfigurationException
from maze import Cell, create_grid, define_start_position
from maze import generate_output_file
import sys

def draw_maze(grid: list[list[Cell]], config: Config) -> None:
    for y, row in enumerate(grid):
        for cell in row:
            print("•", end="")
            print("───" if cell.top else "   ", end="")
        print("•")
        for cell in row:
            print("│" if cell.left else " ", end="")

            is_42 = (
                cell.top
                and cell.right
                and cell.bottom
                and cell.left
            )

            if cell.x == config.entry.x and cell.y == config.entry.y:
                print(" E ", end="")
            elif cell.x == config.exit.x and cell.y == config.exit.y:
                print(" X ", end="")
            elif is_42:
                print("███", end="")
            else:
                print("   ", end="")

        last = row[-1]
        print("│" if last.right else "")

    for cell in grid[-1]:
        print("•", end="")
        print("───" if cell.bottom else "   ", end="")
    print("•")

def count_open_walls(grid: list[list[Cell]]) -> int:
    count = 0

    for row in grid:
        for cell in row:
            if cell.right == 0:
                count += 1
            if cell.bottom == 0:
                count += 1

    return count

if __name__ == "__main__":
	# if len(sys.argv) != 2:
	# 	print(
	# 		"Your program must be run with the following command: "
	# 		"python3 a_maze_ing.py file_name.txt"
	# 	)
	# 	exit()
	try:
		config = read_config_file("config.txt")
		# config = read_config_file(sys.argv[1])
		grid = create_grid(config)
		define_start_position(grid, config)
	except ConfigurationException as e:
		print(f"Configuration error: {e}")
		exit()
	# print(count_open_walls(grid))
    
	generate_output_file(grid, config)    
	draw_maze(grid, config)
