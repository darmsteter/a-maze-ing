from maze.models import Cell
from config.models import Config


def generate_output_file(
    grid: list[list[Cell]], config: Config, path: str
) -> None:
    """Write the generated maze and solution path to the output file.

    Args:
        grid: Two-dimensional list containing the generated maze cells.
        config: Maze configuration containing the output file path,
            entry coordinates, and exit coordinates.
        path: String describing the path from the entry to the exit.
    """

    with open(config.output_file, "w") as output_file:
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                cell = grid[y][x]
                output = (
                    pow(2, 0) * cell.top
                    + pow(2, 1) * cell.right
                    + pow(2, 2) * cell.bottom
                    + pow(2, 3) * cell.left
                )
                output_file.write(f"{output:x}")
            output_file.write("\n")
        output_file.write("\n")
        output_file.write(f"{config.entry.x},{config.entry.y}\n")
        output_file.write(f"{config.exit.x},{config.exit.y}\n")
        output_file.write(path)
