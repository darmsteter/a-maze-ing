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

        self.was_visited = 0

        self.was_visited = False
        self.is_42 = False

    def is_wall(self) -> bool:
        return (
            self.top == 1
            and self.right == 1
            and self.bottom == 1
            and self.left == 1
        )

    def is_start(self, config) -> bool:
        return self.x == config.entry.x and self.y == config.entry.y

    def is_exit(self, config) -> bool:
        return self.x == config.exit.x and self.y == config.exit.y


def create_grid(height: int, width: int) -> list[list[Cell]]:
    grid: list[list[Cell]] = []

    for y in range(height):
        row: list[Cell] = []
        for x in range(width):
            row.append(Cell(x=x, y=y))
        grid.append(row)
    return grid
