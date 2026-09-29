from enum import IntEnum


class Directions(IntEnum):
    """Represent the four possible directions in the maze."""

    TOP = 0
    RIGHT = 1
    BOTTOM = 2
    LEFT = 3


DIRECTIONS = (
    (Directions.TOP, 0, -1),
    (Directions.RIGHT, 1, 0),
    (Directions.BOTTOM, 0, 1),
    (Directions.LEFT, -1, 0),
)


class Cell:
    """Represent a single cell of the maze."""

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

        self.top = 1
        self.right = 1
        self.bottom = 1
        self.left = 1

        self.was_visited = False
        self.is_42 = False

    def is_wall(self) -> bool:
        """Check whether the cell is surrounded by walls.

        Returns:
            True if all four sides of the cell have walls, otherwise False.
        """

        return (
            self.top == 1
            and self.right == 1
            and self.bottom == 1
            and self.left == 1
        )


def create_grid(height: int, width: int) -> list[list[Cell]]:
    """Create a two-dimensional grid of maze cells.

    Args:
        height: Number of rows in the grid.
        width: Number of columns in the grid.

    Returns:
        A two-dimensional list containing initialized Cell objects.
    """
    
    grid: list[list[Cell]] = []

    for y in range(height):
        row: list[Cell] = []
        for x in range(width):
            row.append(Cell(x=x, y=y))
        grid.append(row)
    return grid
