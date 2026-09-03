from config.models import Config, Pair
from .models import Cell
import random
from errors import ConfigurationException
from .find_path  import find_path

def add_42(grid: list[list[Cell]], config: Config):
	if len(grid) < 7 or len(grid[0]) < 5:
		print('The maze is too small to display "42" in the center.')
		return 0
	pattern = [
		"x...xxx",
		"x.....x",
		"xxx.xxx",
		"..x.x..",
		"..x.xxx"
	]
	
	start_x = int((len(grid[0]) - len(pattern[0])) / 2)
	if len(grid[0]) % 2 == 0:
		start_x += 1
	start_y = int((len(grid) - len(pattern)) / 2)
	pattern_counter = 0
	for y in range(len(pattern)):
		for x in range(len(pattern[y])):
			if pattern[y][x] != 'x':
				continue
			if start_x + x == config.entry.x and start_y + y == config.entry.y:
				raise ConfigurationException("Entry cannot be inside 42.")
			if start_x + x == config.exit.x and start_y + y == config.exit.y:
				raise ConfigurationException("Exit cannot be inside 42.")
			grid[start_y + y][start_x + x].was_visited = 1
			grid[start_y + y][start_x + x].is_42 = 1
			pattern_counter += 1
	return pattern_counter

def define_start_position(grid: list[list[Cell]], config: Config) -> str:
	try:
		pattern = add_42(grid, config)
	except ConfigurationException as e:
		raise ConfigurationException(e)
	random.seed(config.seed)
	while True:
		coordinate = Pair(
			x=random.randrange(0, config.width),
			y=random.randrange(0, config.height)
			)
		point = grid[coordinate.y][coordinate.x]
		if not point.was_visited:
			point.was_visited = 1
			break
	# prims(grid, point)
	generate_maze(grid, 1 + pattern, point)
	return find_path(config, grid)


def break_wall(current: Cell, next: Cell, direction: int):
	match direction:
		case 0:
			current.top = 0
			next.bottom = 0
		case 1:
			current.right = 0
			next.left = 0
		case 2:
			current.bottom = 0
			next.top = 0
		case 3:
			current.left = 0
			next.right = 0

def find_neighbours(grid: list[list[Cell]], cell: Cell) -> dict[int, Cell]:
	neighbours: dict[int, Cell] = {}
	if cell.y - 1 >= 0:
		neighbour = grid[cell.y - 1][cell.x]
		if not neighbour.was_visited:
			neighbours[0] = neighbour
	if cell.x + 1 <= len(grid[0]) - 1:
		neighbour = grid[cell.y][cell.x + 1]
		if not neighbour.was_visited:
			neighbours[1] = neighbour
	if cell.y + 1 <= len(grid) - 1:
		neighbour = grid[cell.y + 1][cell.x]
		if not neighbour.was_visited:
			neighbours[2] = neighbour
	if cell.x - 1 >= 0:
		neighbour = grid[cell.y][cell.x - 1]
		if not neighbour.was_visited:
			neighbours[3] = neighbour
	return neighbours

def find_visited_neighbours(grid: list[list[Cell]], cell: Cell):
	neighbours: dict[int, Cell] = {}
	if cell.y - 1 >= 0:
		neighbour = grid[cell.y - 1][cell.x]
		if neighbour.was_visited and not neighbour.is_42:
			neighbours[0] = neighbour
	if cell.x + 1 <= len(grid[0]) - 1:
		neighbour = grid[cell.y][cell.x + 1]
		if neighbour.was_visited and not neighbour.is_42:
			neighbours[1] = neighbour
	if cell.y + 1 <= len(grid) - 1:
		neighbour = grid[cell.y + 1][cell.x]
		if neighbour.was_visited and not neighbour.is_42:
			neighbours[2] = neighbour
	if cell.x - 1 >= 0:
		neighbour = grid[cell.y][cell.x - 1]
		if neighbour.was_visited and not neighbour.is_42:
			neighbours[3] = neighbour
	return neighbours


def generate_maze(grid: list[list[Cell]], visited_count: int, cell: Cell):
	if visited_count == len(grid) * len(grid[0]):
		return 1
	neighbours = find_neighbours(grid, cell)
	while neighbours:
		direction = random.randrange(0, 4)
		if direction not in neighbours:
			continue
		next_cell = neighbours[direction]
		next_cell.was_visited = 1
		break_wall(cell, next_cell, direction)
		if generate_maze(grid, visited_count + 1, next_cell):
			return 1
		neighbours = find_neighbours(grid, cell)
		continue
	return 0

def prims(grid: list[list[Cell]], cell: Cell):
	frontier = []
	for value in find_neighbours(grid, cell).values():
		frontier.append(value)
	while frontier:
		current_cell = random.choice(frontier)
		visited_neighbours = find_visited_neighbours(grid, current_cell)
		direction = random.choice(list(visited_neighbours))
		break_wall(current_cell, visited_neighbours[direction], direction)
		frontier.remove(current_cell)
		grid[current_cell.y][current_cell.x].was_visited = 1
		for value in find_neighbours(grid, current_cell).values():
			if value not in frontier: 
				frontier.append(value)