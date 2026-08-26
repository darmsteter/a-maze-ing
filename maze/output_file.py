from maze.models import Cell
from config.models import Config

def generate_output_file(grid: list[list[Cell]], config: Config):
	with open(config.output_file, 'w') as output_file:
		for y in range(len(grid)):
			for x in range(len(grid[y])):
				cell = grid[y][x]
				output = pow(2, 0) * cell.top + pow(2, 1) * cell.right + pow(2, 2) * cell.bottom + pow(2, 3) * cell.left
				output_file.write(f"{output:x}")
			output_file.write('\n')
		output_file.write('\n')
		output_file.write(f"{config.entry.x, config.entry.y}    # entry (x,y)\n")
		output_file.write(f"{config.exit.x, config.exit.y}    # exit (x,y)\n")
