from config.models import Config
from maze.models import Cell


def to_display_grid(
        grid: list[list[Cell]], width: int, height: int, config: Config
) -> list[list[str]]:
    out_w = width * 2 + 1
    out_h = height * 2 + 1
    display = [['W' for _ in range(out_w)] for _ in range(out_h)]

    for y in range(height):
        for x in range(width):
            cell = grid[y][x]
            gx, gy = x * 2 + 1, y * 2 + 1

            # Identify '42', start, exit and path
            if getattr(cell, 'is_42', False):
                display[gy][gx] = '4'
            elif cell.is_start(config):
                display[gy][gx] = 'S'
            elif cell.is_exit(config):
                display[gy][gx] = 'E'
            else:
                display[gy][gx] = ' '

            # Colors
            if not cell.top:
                display[gy - 1][gx] = ' '
            if not cell.bottom:
                display[gy + 1][gx] = ' '
            if not cell.left:
                display[gy][gx - 1] = ' '
            if not cell.right:
                display[gy][gx + 1] = ' '

    return display
