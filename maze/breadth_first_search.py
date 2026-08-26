from config.models import Config, Pair
from .models import Cell
from collections import deque

# def find_

def find_path(grid: list[list[Cell]], config: Config):
	frontier = deque[grid[config.entry.y][config.entry.x]]
	visited_vertex: list[Cell]  = [grid[config.entry.y][config.entry.x]]
	previous: dict[str, str]

	while True:
		if 

