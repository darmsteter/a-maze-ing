MAIN = a_maze_ing.py
CONFIG = config.txt
FLAGS = --warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs

all: run

install:
	uv sync

run:
	uv run python3 $(MAIN) $(CONFIG)
 
debug:
	uv run python3 -m pdb $(MAIN) $(CONFIG)

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .mypy_cache -exec rm -rf {} +

lint:
	flake8 .
	mypy . $(FLAGS)

lint-strict:
	flake8 .
	mypy . --strict

.PHONY: install run debug clean lint lint-strict