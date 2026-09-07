from heapq import heappush, heappop
from typing import Callable

from config.models import Config
from maze.models import Cell, DIRECTIONS


def maze_counter() -> Callable[[], int]:
	count = 0

	def counter() -> int:
		nonlocal count
		count += 1
		return count

	return counter

def manhattan_distance(x1: int, x2: int, y1: int, y2: int) -> int:
	return abs(x1 - x2) + abs(y1 - y2)

def update_neighbours(
		cell: Cell,
		frontier: list[tuple[int, int, tuple[int, int]]],
		g_score: dict[tuple[int, int], int],
		exit: tuple[int, int],
		counter: Callable[[], int], 
		came_from: dict[tuple[int, int], tuple[int, int]]
) -> None:
	walls = (cell.top, cell.right, cell.bottom, cell.left)
	for direction, dir_x, dir_y in DIRECTIONS:
		if walls[direction]:
			continue

		neighbour = (cell.x + dir_x, cell.y + dir_y)
		tentative_g_score = g_score[(cell.x, cell.y)] + 1
		if neighbour not in g_score or tentative_g_score < g_score[neighbour]:
			g_score[neighbour] = tentative_g_score
			came_from[neighbour] = (cell.x, cell.y)
			h_score = manhattan_distance(neighbour[0], exit[0], neighbour[1], exit[1])
			f_score = h_score + g_score[neighbour]
			heappush(frontier, (f_score, counter(), neighbour))


def compile_path(
		entry: tuple[int, int],
		came_from: dict[tuple[int, int], tuple[int, int]], 
		exit: tuple[int, int]) -> str:
	current = exit
	path: list[str] = []
	while current != entry:
		previous_cell = came_from[current]
		if previous_cell[0] < current[0]:
			path.append('E')
		elif previous_cell[0] > current[0]:
			path.append('W')
		elif previous_cell[1] < current[1]:
			path.append('S')
		elif previous_cell[1] > current[1]:
			path.append('N')
		current = previous_cell
	path.reverse()
	return ''.join(path)


def find_path(config: Config, grid: list[list[Cell]]) -> str:
	exit = (config.exit.x, config.exit.y)
	entry = (config.entry.x, config.entry.y)
	frontier: list[tuple[int, int, tuple[int, int]]] = []
	g_score = {
		entry: 0
		}
	counter = maze_counter()
	came_from: dict[tuple[int, int], tuple[int, int]] = {}
	heappush(frontier, (0, counter(), entry))
	while frontier:
		_, _, current_cell = heappop(frontier)
		if current_cell == exit:
			break
		update_neighbours(
			grid[current_cell[1]][current_cell[0]],
			frontier,
			g_score,
			exit,
			counter,
			came_from
		)
	return compile_path(entry, came_from, exit)