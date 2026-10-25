# Game of Life 🔫

> **Difficulty:** 🌶️🌶️
>
> **Before you start:** basic Python and NumPy, and the optional scientific stack
> (`uv sync --all-groups --extra science`).
>
> **You’ll practise:** NumPy arrays and slicing, neighbourhood calculations,
> and simulating a cellular automaton.
>
> **Check:** `uv run pytest exercises/models_of_life/game_of_life/ -q`

Conway's Game of Life is a cellular automaton: a grid of live and dead cells
changes in discrete generations according to local rules. The rules fit in a
paragraph. What they produce does not. Your job is to write the engine; the
reward is watching what it does.

For each cell, inspect its eight neighbouring positions. Follow these rules:
1. A live cell survives with two or three live neighbours
2. A dead cell becomes live with exactly three;
3. All other cells are dead in the next generation.

This exercise uses finite, bounded arrays rather than wrapping edges, so cells
outside the board are not counted.

In [game_of_life.py](game_of_life.py), implement
`count_live_neighbors` and `step_game_of_life` with NumPy arrays; the docstrings
give the details. Consider shifted array slices or padding to vectorise the local
counts without accidentally wrapping edges. Everything else is provided:
readable patterns in
[game_of_life_shapes.yaml](data/game_of_life_shapes.yaml)
(`O` for live cells, `.` for empty ones), `load_shape` and `place_shape` to put
one on a board, `render_board` to print it, and `animate_boards` to watch it
move, so you can focus on the algorithm.

When the tests pass, open the [Game of Life notebook](investigate.ipynb).
Start with the glider, then take on the final challenge: can you build a machine
that makes more machines? Load the "Gosper Glider Gun", only 36 cells, and see
whether it can repeatedly create something that travels across the grid. The last
test, which counts how a 36-cell pattern grows over time, is the check that you
have built it.
