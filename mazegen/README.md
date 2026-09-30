# mazegen

`mazegen` is a reusable Python package for generating random mazes.

The package provides the `MazeGenerator` class, which supports different maze generation algorithms, reproducible generation with a seed, perfect and imperfect mazes, and access to the generated maze structure.

## Requirements

* Python 3.10 or later
* No third-party dependencies

## Installation

Install the package from the wheel:

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

## Quick start

```python
from mazegen.generate_maze import MazeGenerator

generator = MazeGenerator()

grid = generator.generate(
    height=15,
    width=15,
    entry=(0, 0),
    exit=(14, 14),
    seed=42,
    perfect="True",
    algorithm="dfs",
)

print(grid)
```

`generate()` returns the generated maze as a two-dimensional grid of `Cell` objects.

## Generate a maze with custom parameters

```python
grid = generator.generate(
    height=20,
    width=30,
    entry=(0, 0),
    exit=(29, 19),
    seed=123,
    perfect="True",
    algorithm="prim",
)
```

### Parameters

| Parameter   | Type               | Description                                                |
| ----------- | ------------------ | ---------------------------------------------------------- |
| `height`    | `int`              | Number of rows in the maze                                 |
| `width`     | `int`              | Number of columns in the maze                              |
| `entry`     | `tuple[int, int]`  | Entry coordinates `(x, y)`                                 |
| `exit`      | `tuple[int, int]`  | Exit coordinates `(x, y)`                                  |
| `seed`      | `int \| None`      | Optional random seed for reproducible generation           |
 `perfect` | `str` | `"True"` to generate a perfect maze, `"False"` to allow additional passages |
| `algorithm` | `str`              | Maze generation algorithm, for example `"dfs"` or `"prim"` |
| `callback`  | `callable \| None` | Optional callback used during generation                   |

The same seed and generation parameters produce the same maze.

## Generated maze structure

The generated maze is returned as:

```python
list[list[Cell]]
```

Each cell contains four wall values:

```python
cell.top
cell.right
cell.bottom
cell.left
```

A value of `1` means that the wall is closed and `0` means that the wall is open.

Each cell also contains:

```python
cell.x
cell.y
cell.visited
cell.is_42
```

Example:

```python
cell = grid[0][0]

print(cell.x)
print(cell.y)
print(cell.top)
print(cell.right)
print(cell.bottom)
print(cell.left)
```

The grid is indexed as:

```python
grid[y][x]
```

where `y` is the row and `x` is the column.

## Maze generation algorithms

The package supports:

### DFS

Depth-first search (recursive backtracking) creates a perfect maze when `perfect=True`.

```python
grid = generator.generate(
    height=15,
    width=15,
    entry=(0, 0),
    exit=(14, 14),
    seed=42,
    perfect="True",
    algorithm="dfs",
)
```

### Prim

Prim's algorithm can also be used to generate the maze.

```python
grid = generator.generate(
    height=15,
    width=15,
    entry=(0, 0),
    exit=(14, 14),
    seed=42,
    perfect="True",
    algorithm="prim",
)
```

## Perfect and imperfect mazes

When `perfect="True"`, the generated maze is a perfect maze: there is exactly one route between two connected cells.

When `perfect="False"`, additional passages can be opened to create multiple routes through the maze.

```python
grid = generator.generate(
    height=15,
    width=15,
    entry=(0, 0),
    exit=(14, 14),
    seed=42,
    perfect="False",
    algorithm="dfs",
)
```

## Reproducible generation

A seed can be provided to make generation reproducible:

```python
grid_1 = generator.generate(
    15,
    15,
    (0, 0),
    (14, 14),
    seed=42,
    perfect="True",
    algorithm="dfs",
)

grid_2 = generator.generate(
    15,
    15,
    (0, 0),
    (14, 14),
    seed=42,
    perfect="True",
    algorithm="dfs",
)
```

Using the same parameters and seed produces the same maze.

## Errors

Invalid maze generation parameters raise `MazeGenerationError`.

For example, an entry or exit placed inside the `42` pattern cannot be used.

```python
from mazegen.errors import MazeGenerationError
```

## Public API

### `MazeGenerator`

```python
from mazegen.generate_maze import MazeGenerator
```

Main method:

```python
MazeGenerator.generate(...)
```

Returns:

```python
list[list[Cell]]
```

### `Cell`

```python
from mazegen.models import Cell
```

Represents a single maze cell and stores its coordinates, walls and generation state.

## Example

```python
from mazegen.generate_maze import MazeGenerator

generator = MazeGenerator()

grid = generator.generate(
    height=15,
    width=20,
    entry=(0, 0),
    exit=(19, 14),
    seed=42,
    perfect="True",
    algorithm="dfs",
)

path = find_path(
    grid,
    (0, 0),
    (19, 14),
)

print(f"Maze size: {len(grid)} x {len(grid[0])}")
print(f"Solution: {path}")
```

## Package contents

```text
mazegen/
├── __init__.py
├── errors.py
├── generate_maze.py
└── models.py
```

* `generate_maze.py` — maze generation
* `models.py` — maze data structures
* `errors.py` — maze generation exceptions

## Authors

* Carmen-Elena Bruma
* Svetlana Koreneva
