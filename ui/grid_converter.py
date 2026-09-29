from config.models import Config
from mazegen.models import Cell
from .cell_helpers import is_start, is_exit


def to_display_grid(
    grid: list[list[Cell]], width: int, height: int, config: Config
) -> list[list[str]]:
    """Convert the maze grid into a grid suitable for display.

    The resulting grid represents maze cells, walls, the 42 pattern,
    the entry, and the exit using single-character symbols.

    Args:
        grid: Two-dimensional list containing the maze cells.
        width: Number of cells in each row of the maze.
        height: Number of rows in the maze.
        config: Maze configuration containing the entry and exit positions.

    Returns:
        A two-dimensional list of strings representing the maze for display.
    """

    display_width = width * 2 + 1
    display_height = height * 2 + 1
    display_grid = [
        ["W" for _ in range(display_width)] for _ in range(display_height)
    ]

    for cell_y in range(height):
        for cell_x in range(width):
            current_cell = grid[cell_y][cell_x]
            render_x, render_y = cell_x * 2 + 1, cell_y * 2 + 1

            is_42 = getattr(current_cell, "is_42", False)

            top_neighbor_is_42 = cell_y > 0 and getattr(
                grid[cell_y - 1][cell_x], "is_42", False
            )
            bottom_neighbor_is_42 = cell_y < height - 1 and getattr(
                grid[cell_y + 1][cell_x], "is_42", False
            )
            right_neighbor_is_42 = cell_x < width - 1 and getattr(
                grid[cell_y][cell_x + 1], "is_42", False
            )
            left_neighbor_is_42 = cell_x > 0 and getattr(
                grid[cell_y][cell_x - 1], "is_42", False
            )

            if is_42:
                display_grid[render_y][render_x] = "4"
            elif is_start(current_cell, config):
                display_grid[render_y][render_x] = "S"
            elif is_exit(current_cell, config):
                display_grid[render_y][render_x] = "E"
            else:
                display_grid[render_y][render_x] = " "

            if is_42 and top_neighbor_is_42:
                display_grid[render_y - 1][render_x] = "4"
            elif not current_cell.top:
                display_grid[render_y - 1][render_x] = " "

            if is_42 and bottom_neighbor_is_42:
                display_grid[render_y + 1][render_x] = "4"
            elif not current_cell.bottom:
                display_grid[render_y + 1][render_x] = " "

            if is_42 and left_neighbor_is_42:
                display_grid[render_y][render_x - 1] = "4"
            elif not current_cell.left:
                display_grid[render_y][render_x - 1] = " "

            if is_42 and right_neighbor_is_42:
                display_grid[render_y][render_x + 1] = "4"
            elif not current_cell.right:
                display_grid[render_y][render_x + 1] = " "

    return display_grid
