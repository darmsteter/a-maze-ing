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
            is_42 = getattr(cell, 'is_42', False)

            top_is_42 = y > 0 and getattr(grid[y - 1][x], 'is_42', False)
            bottom_is_42 = y < height - 1 and getattr(
                grid[y + 1][x], 'is_42', False)
            right_is_42 = x < width - 1 and getattr(
                grid[y][x + 1], 'is_42', False)
            left_is_42 = x > 0 and getattr(grid[y][x - 1], 'is_42', False)

            # Identify '42', start, exit and path
            if is_42:
                display[gy][gx] = '4'
            elif cell.is_start(config):
                display[gy][gx] = 'S'
            elif cell.is_exit(config):
                display[gy][gx] = 'E'
            else:
                display[gy][gx] = ' '

            # Colors
            if is_42 and top_is_42:
                display[gy - 1][gx] = '4'
            elif not cell.top:
                display[gy - 1][gx] = ' '

            if is_42 and bottom_is_42:
                display[gy + 1][gx] = '4'
            elif not cell.bottom:
                display[gy + 1][gx] = ' '

            if is_42 and left_is_42:
                display[gy][gx - 1] = '4'
            elif not cell.left:
                display[gy][gx - 1] = ' '

            if is_42 and right_is_42:
                display[gy][gx + 1] = '4'
            elif not cell.right:
                display[gy][gx + 1] = ' '

    return display
