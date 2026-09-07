import random
from config import Config, read_config_file
from errors import ConfigurationException
from maze import create_grid
from maze.models import Cell


def to_display_grid(grid: list[list[Cell]], width: int, height: int):
    # Creează o grilă extinsă plină de ziduri ('W')
    out_w = width * 2 + 1
    out_h = height * 2 + 1
    display = [['W' for _ in range(out_w)] for _ in range(out_h)]

    for y in range(height):
        for x in range(width):
            cell = grid[y][x]
            gx, gy = x * 2 + 1, y * 2 + 1
            
            display[gy][gx] = ' '  # Drumul interior

            if not cell.top:
                display[gy - 1][gx] = ' '
            if not cell.bottom:
                display[gy + 1][gx] = ' '
            if not cell.left:
                display[gy][gx - 1] = ' '
            if not cell.right:
                display[gy][gx + 1] = ' '

    return display


def validate_dimensions(width: int, height: int):
    """Ensure the maze has a minimum viable size."""
    if width < 5 or height < 5:
        raise ConfigurationException(
            f"Maze dimensions must be at least 5x5 (got {width}x{height})."
        )


def validate_coords(x: int, y: int, width: int, height: int, label: str):
    """Ensure a coordinate falls within the maze bounds."""
    if not (0 <= x < width) or not (0 <= y < height):
        raise ConfigurationException(
            f"{label} coordinates ({x}, {y}) are outside the maze bounds "
            f"({width}x{height})."
        )


def break_wall_between(current: Cell, neighbor: Cell, dx: int, dy: int):
    """Break the wall between two cells based on the direction of movement."""
    if dx == 1:  # Est
        current.right = 0
        neighbor.left = 0
    elif dx == -1:  # West
        current.left = 0
        neighbor.right = 0
    elif dy == 1:  # South
        current.bottom = 0
        neighbor.top = 0
    elif dy == -1:  # North
        current.top = 0
        neighbor.bottom = 0


def carve_maze(grid: list[list[Cell]], width: int, height: int):
    """Carve paths into the maze grid using iterative DFS backtracking."""
    stack = [grid[0][0]]
    grid[0][0].was_visited = 1
    moves = [(0, -1), (1, 0), (0, 1), (-1, 0)]  # N, E, S, W

    while stack:
        current = stack[-1]
        unvisited_neighbors = []

        for dx, dy in moves:
            nx, ny = current.x + dx, current.y + dy
            if 0 <= nx < width and 0 <= ny < height:
                neighbor = grid[ny][nx]
                if not neighbor.was_visited:
                    unvisited_neighbors.append((neighbor, dx, dy))

        if not unvisited_neighbors:
            stack.pop()
            continue

        chosen_neighbor, dx, dy = random.choice(unvisited_neighbors)

        # Break down the wall between the current cell and the neighbor
        break_wall_between(current, chosen_neighbor, dx, dy)

        chosen_neighbor.was_visited = 1
        stack.append(chosen_neighbor)


def generate_maze(config: Config) -> list[list[Cell]]:
    """
    Generate the maze grid of Cell objects and validates start/exit parameters.
    """
    width = config.width
    height = config.height

    validate_dimensions(width, height)

    entry_x = int(config.entry.x)
    entry_y = int(config.entry.y)
    exit_x = int(config.exit.x)
    exit_y = int(config.exit.y)

    validate_coords(entry_x, entry_y, width, height, "Entry")
    validate_coords(exit_x, exit_y, width, height, "Exit")

    if (entry_x, entry_y) == (exit_x, exit_y):
        raise ConfigurationException(
            "Entry and exit cannot be at the same position."
        )

    # 1. Cream grila de obiecte Cell folosind functia existenta
    grid = create_grid(config)

    # 2. Executam algoritmul DFS pentru a sparge peretii
    carve_maze(grid, width, height)

    return grid