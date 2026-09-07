from enum import IntEnum

class Directions(IntEnum):
    TOP = 0
    RIGHT = 1
    BOTTOM = 2
    LEFT = 3

DIRECTIONS = (
		(Directions.TOP, 0, -1),
		(Directions.RIGHT, 1, 0),
		(Directions.BOTTOM, 0, 1),
		(Directions.LEFT, -1, 0)
		)

class Cell:
	def __init__(self, x: int, y: int):
		self.x = x
		self.y = y

		self.top = 1
		self.right = 1
		self.bottom = 1
		self.left = 1

		self.was_visited = False
		self.is_42 = False

def create_grid(height: int, width: int) -> list[list[Cell]]:
	grid: list[list[Cell]] = []

	for y in range(height):
		row: list[Cell] = []
		for x in range(width):
			row.append(Cell(x=x, y=y))
		grid.append(row)
	return grid