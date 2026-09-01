from heapq import heappush, heappop
from config.models import Config
from maze.models import Cell
from typing import Callable

def maze_counter() -> Callable[[], int]:
    count = 0

    def counter() -> int:
        nonlocal count
        count += 1
        return count

    return counter

def get_h_score(x1: int, x2: int, y1: int, y2: int) -> int:
	return abs(x1 - x2) + abs(y1 - y2)

def handle_neibghours(
		cell: Cell,
		frontier,
		g_score,
		exit,
		counter, 
		came_from
):
	tentative_g_score = g_score[(cell.x, cell.y)] + 1
	if not cell.top:
		neibghour = (cell.x, cell.y - 1)
		if neibghour not in g_score or tentative_g_score < g_score[neibghour]:
			g_score[neibghour] = tentative_g_score
			came_from[neibghour] = (cell.x, cell.y)
			f_score = get_h_score(neibghour[0], exit[0], neibghour[1], exit[1]) + g_score[neibghour]
			heappush(frontier, (f_score, counter(), neibghour))
	if not cell.right:
		neibghour = (cell.x + 1, cell.y)
		if neibghour not in g_score or tentative_g_score < g_score[neibghour]:
			g_score[neibghour] = tentative_g_score
			came_from[neibghour] = (cell.x, cell.y)
			f_score = get_h_score(neibghour[0], exit[0], neibghour[1], exit[1]) + g_score[neibghour]
			heappush(frontier, (f_score, counter(), neibghour))
	if not cell.bottom:
		neibghour = (cell.x, cell.y + 1)
		if neibghour not in g_score or tentative_g_score < g_score[neibghour]:
			g_score[neibghour] = tentative_g_score
			came_from[neibghour] = (cell.x, cell.y)
			f_score = get_h_score(neibghour[0], exit[0], neibghour[1], exit[1]) + g_score[neibghour]
			heappush(frontier, (f_score, counter(), neibghour))
	if not cell.left:
		neibghour = (cell.x - 1, cell.y)
		if neibghour not in g_score or tentative_g_score < g_score[neibghour]:
			g_score[neibghour] = tentative_g_score
			came_from[neibghour] = (cell.x, cell.y)
			f_score = get_h_score(neibghour[0], exit[0], neibghour[1], exit[1]) + g_score[neibghour]
			heappush(frontier, (f_score, counter(), neibghour))
	

def find_path(config: Config, grid: list[list[Cell]]) -> str:
	exit = (config.exit.x, config.exit.y)
	frontier = []
	g_score = {
		(config.entry.x, config.entry.y): 0
		}
	counter = maze_counter()
	came_from = {}
	handle_neibghours(
		grid[config.entry.y][config.entry.x],
		frontier,
		g_score,
		exit,
		counter,
		came_from
	)
	while frontier:
		_, _, current_cell = heappop(frontier)
		if current_cell == exit:
			break
		handle_neibghours(
			grid[current_cell[1]][current_cell[0]],
			frontier,
			g_score,
			exit,
			counter,
			came_from
		)
	entry = (config.entry.x, config.entry.y)
	cell = exit
	path = []
	while cell != entry:
		cell_from = came_from[cell]
		if cell_from[0] < cell[0]:
			path.append('E')
		elif cell_from[0] > cell[0]:
			path.append('W')
		elif cell_from[1] < cell[1]:
			path.append('S')
		elif cell_from[1] > cell[1]:
			path.append('N')
		cell = cell_from
	path.reverse()

	return ''.join(path)