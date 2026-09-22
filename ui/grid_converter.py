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
            grid_x, grid_y = x * 2 + 1, y * 2 + 1
            is_42 = getattr(cell, 'is_42', False)

            top_is_42 = y > 0 and getattr(grid[y - 1][x], 'is_42', False)
            bottom_is_42 = y < height - 1 and getattr(
                grid[y + 1][x], 'is_42', False)
            right_is_42 = x < width - 1 and getattr(
                grid[y][x + 1], 'is_42', False)
            left_is_42 = x > 0 and getattr(grid[y][x - 1], 'is_42', False)

            # Identify '42', start, exit and path
            if is_42:
                display[grid_y][grid_x] = '4'
            elif cell.is_start(config):
                display[grid_y][grid_x] = 'S'
            elif cell.is_exit(config):
                display[grid_y][grid_x] = 'E'
            else:
                display[grid_y][grid_x] = ' '

            # Colors
            if is_42 and top_is_42:
                display[grid_y - 1][grid_x] = '4'
            elif not cell.top:
                display[grid_y - 1][grid_x] = ' '

            if is_42 and bottom_is_42:
                display[grid_y + 1][grid_x] = '4'
            elif not cell.bottom:
                display[grid_y + 1][grid_x] = ' '

            if is_42 and left_is_42:
                display[grid_y][grid_x - 1] = '4'
            elif not cell.left:
                display[grid_y][grid_x - 1] = ' '

            if is_42 and right_is_42:
                display[grid_y][grid_x + 1] = '4'
            elif not cell.right:
                display[grid_y][grid_x + 1] = ' '

    return display
