import abc
import random

from errors import ConfigurationException

from .find_path import find_path
from .models import Cell, Directions, DIRECTIONS


class MazeGenerator():
    def __init__(self) -> None:
        self.marked_cells = 0

    def create_grid(self, height: int, width: int) -> list[list[Cell]]:
        grid: list[list[Cell]] = []
        for y in range(height):
            row: list[Cell] = []
            for x in range(width):
                row.append(Cell(x=x, y=y))
            grid.append(row)
        return grid


    def add_42(self, grid: list[list[Cell]], entry: tuple[int, int], exit: tuple[int, int]) -> None:
        if len(grid) < 7 or len(grid[0]) < 5:
            print('The maze is too small to display "42" in the center.')
            return
        pattern = [
            "x...xxx",
            "x.....x",
            "xxx.xxx",
            "..x.x..",
            "..x.xxx"
        ]
        pattern_height = len(pattern)
        pattern_width = len(pattern[0])
        start_x = (len(grid[0]) - pattern_width) // 2
        if len(grid[0]) % 2 == 0:
            start_x += 1
        start_y = (len(grid) - pattern_height) // 2
        for y in range(pattern_height):
            for x in range(pattern_width):
                position = (start_x + x, start_y + y)
                if pattern[y][x] != 'x':
                    continue
                if position == entry:
                    raise ConfigurationException("Entry cannot be inside 42.")
                if position == exit:
                    raise ConfigurationException("Exit cannot be inside 42.")
                grid[start_y + y][start_x + x].is_42 = True
                self.marked_cells += 1

    def generate(self, height: int, width: int, entry: tuple[int, int], exit: tuple[int, int], seed: int | None, perfect: bool, algorithm: str) -> tuple[list[list[Cell]], str]:
        grid = self.create_grid(height, width)
        self.marked_cells = 0
        self.add_42(grid, entry, exit)
        random.seed(seed)
        while True:
            x = random.randrange(width)
            y = random.randrange(height)
            cell = grid[y][x]
            if cell.is_42:
                continue
            cell.was_visited = True
            break
        if algorithm.lower() == 'prim':
            self._generate_prim(grid, cell)
        else:
            self._generate_dfs(grid, cell)
        if perfect == False:
            self.imperfect_maze(grid)
        return grid, find_path(exit, entry, grid)


    def break_wall(self, current: Cell, neighbour: Cell, direction: Directions) -> None:
        match direction:
            case Directions.TOP:
                current.top = 0
                neighbour.bottom = 0
            case Directions.RIGHT:
                current.right = 0
                neighbour.left = 0
            case Directions.BOTTOM:
                current.bottom = 0
                neighbour.top = 0
            case Directions.LEFT:
                current.left = 0
                neighbour.right = 0

    def find_neighbours(self, grid: list[list[Cell]], cell: Cell, visited: bool) -> dict[Directions, Cell]:
        neighbours: dict[Directions, Cell] = {}
        for direction, dir_x, dir_y in DIRECTIONS:
            x = cell.x + dir_x
            y = cell.y + dir_y
            if not (0 <= x < len(grid[0]) and 0 <= y < len(grid)):
                continue
            neighbour = grid[y][x]

            if neighbour.was_visited == visited and not neighbour.is_42:
                neighbours[direction] = neighbour
        return neighbours

    def find_walled_neighbours(self, grid: list[list[Cell]], cell: Cell) -> dict[Directions, Cell]:
        neighbours: dict[Directions, Cell] = {}
        walls = (cell.top, cell.right, cell.bottom, cell.left)
        for direction, dir_x, dir_y in DIRECTIONS:
            x = cell.x + dir_x
            y = cell.y + dir_y
            if not (0 <= x < len(grid[0]) and 0 <= y < len(grid)):
                continue
            neighbour = grid[y][x]

            if walls[direction] and not neighbour.is_42:
                neighbours[direction] = neighbour
        return neighbours

    def is_dead_end(self, cell: Cell) -> bool:
        return cell.top + cell.right + cell.bottom + cell.left == 3
        

    def find_dead_ends(self, grid: list[list[Cell]]) -> list[Cell]:
        dead_ends: list[Cell] = []
        for y in range(len(grid)):
            for x in range(len(grid[0])):
                if self.is_dead_end(grid[y][x]):
                    dead_ends.append(grid[y][x])
        return dead_ends

    def imperfect_maze(self, grid: list[list[Cell]]) -> None:
        removed_walls = 0
        while True:
            dead_ends = self.find_dead_ends(grid)
            if (len(dead_ends) <= 2 and removed_walls > 2) or not dead_ends:
                break
            cell = random.choice(dead_ends)
            neighbours = self.find_walled_neighbours(grid, cell)
            if not neighbours:
                dead_ends.remove(cell)
                continue
            direction = random.choice(list(neighbours))
            self.break_wall(cell, neighbours[direction], direction)
            removed_walls += 1



    def _generate_prim(self, grid: list[list[Cell]], cell: Cell) -> None:
        frontier = list(
            self.find_neighbours(grid, cell, False).values()
        )
        while frontier:
            current_cell = random.choice(frontier)
            visited_neighbours = self.find_neighbours(grid, current_cell, True)
            direction = random.choice(list(visited_neighbours))
            self.break_wall(current_cell, visited_neighbours[direction], direction)
            frontier.remove(current_cell)
            grid[current_cell.y][current_cell.x].was_visited = True
            for value in self.find_neighbours(grid, current_cell, False).values():
                if value not in frontier: 
                    frontier.append(value)


    def _generate_dfs(self, grid: list[list[Cell]], cell: Cell) -> None: 
        remaining_cells = len(grid) * len(grid[0]) - self.marked_cells
        self.dfs_recursive(grid, remaining_cells, cell)

    def dfs_recursive(self, grid: list[list[Cell]], remaining_cells: int, cell: Cell) -> bool:
        remaining_cells -= 1
        if remaining_cells == 0:
            return True
        neighbours = self.find_neighbours(grid, cell, False)
        while neighbours:
            direction = random.choice(list(neighbours))
            if direction not in neighbours:
                continue
            next_cell = neighbours[direction]
            next_cell.was_visited = True
            self.break_wall(cell, next_cell, direction)
            if self.dfs_recursive(grid, remaining_cells, next_cell):
                return True
            neighbours = self.find_neighbours(grid, cell, False)
        return False
