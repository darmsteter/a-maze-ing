from config.models import Config

class Cell():
	def __init__(self, x: int, y: int):
		self.x = x
		self.y = y

		self.top = 1
		self.right = 1
		self.bottom = 1
		self.left = 1

		self.was_visited = 0

def create_grid(config: Config):
	grid: list[list[Cell]] = []

	for y in range(0, config.height):
		row: list[Cell] = []
		for x in range(0, config.width):
			row.append(Cell(x=x, y=y))
		grid.append(row)
	return grid