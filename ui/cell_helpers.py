from config.models import Config
from mazegen.models import Cell

def is_start(cell: Cell, config: Config) -> bool:
	"""Check whether the cell is the maze entry point.

	Args:
		cell: Maze cell to check.
		config: Maze configuration containing the entry coordinates.

	Returns:
		True if the cell coordinates match the configured entry point,
		otherwise False.
	"""

	return cell.x == int(config.entry.x) and cell.y == int(config.entry.y)

def is_exit(cell: Cell, config: Config) -> bool:
	"""Check whether the cell is the maze exit point.

	Args:
		cell: Maze cell to check.
		config: Maze configuration containing the exit coordinates.

	Returns:
		True if the cell coordinates match the configured exit point,
		otherwise False.
	"""

	return cell.x == int(config.exit.x) and cell.y == int(config.exit.y)