from exercises.sudoku_solver.loaders import load_sudoku_data
from exercises.sudoku_solver.sudoku import sudoku_checker


def test_sudoku_matches_all_packaged_puzzle_answers():
    for puzzle in load_sudoku_data():
        assert sudoku_checker(puzzle["grid"]) is puzzle["answer"]


def test_sudoku_accepts_an_empty_grid():
    assert sudoku_checker([[None] * 9 for _ in range(9)]) is True


def test_sudoku_rejects_a_duplicate_in_each_constraint_group():
    duplicate_row = [[None] * 9 for _ in range(9)]
    duplicate_row[0][0] = duplicate_row[0][8] = 4
    duplicate_column = [[None] * 9 for _ in range(9)]
    duplicate_column[0][0] = duplicate_column[8][0] = 4
    duplicate_box = [[None] * 9 for _ in range(9)]
    duplicate_box[0][0] = duplicate_box[2][2] = 4

    assert sudoku_checker(duplicate_row) is False
    assert sudoku_checker(duplicate_column) is False
    assert sudoku_checker(duplicate_box) is False
