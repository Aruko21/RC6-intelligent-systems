import numpy as np
import time

import solver as slv
import board as brd
import plotter as plt


N = 4

# variant 8 (4x4)
base_sudoku = np.array([
    [3, 5, 0, 0,   0, 0, 0, 0,   12, 0, 0, 2,   0, 0, 1, 7],
    [0, 14, 13, 0, 0, 0, 16, 0,  8, 0, 5, 1,    15, 0, 0, 0],
    [0, 0, 12, 0,  14, 0, 0, 7,  0, 9, 0, 0,    0, 3, 0, 0],
    [8, 0, 4, 16,  11, 0, 12, 0, 0, 0, 0, 0,    13, 0, 0, 0],

    [0, 6, 0, 0,   0, 0, 8, 0,   5, 0, 0, 12,   0, 4, 2, 9],
    [0, 15, 0, 12, 9, 13, 0, 10, 11, 0, 0, 0,   0, 1, 6, 0],
    [0, 0, 0, 4,   0, 0, 0, 12,  3, 6, 0, 0,    0, 0, 0, 15],
    [5, 1, 0, 0,   0, 3, 0, 11,  0, 0, 4, 14,   0, 0, 13, 0],

    [0, 8, 0, 0,   0, 0, 3, 0,   0, 7, 0, 0,    0, 0, 16, 0],
    [0, 0, 0, 0,   0, 9, 13, 14, 0, 16, 0, 0,   0, 0, 11, 12],
    [2, 0, 11, 0,  1, 0, 0, 0,   6, 0, 8, 0,    0, 10, 0, 0],
    [0, 0, 0, 0,   8, 0, 0, 0,   0, 0, 10, 0,   0, 5, 0, 6],

    [11, 0, 0, 10, 16, 6, 0, 9,  0, 0, 0, 7,    0, 2, 0, 1],
    [4, 13, 0, 0,  0, 0, 0, 0,   0, 0, 16, 5,   0, 0, 14, 0],
    [0, 0, 9, 1,   0, 0, 0, 0,   15, 14, 11, 0, 8, 12, 7, 5],
    [0, 3, 0, 0,   0, 2, 0, 0,   0, 0, 1, 0,    0, 0, 4, 0]
], dtype=int)


def main():
    board = brd.SudokuBoard(base_sudoku)

    solver = slv.SudokuSolver(board)
    # fitness = solver.fitness_func(board)

    # return
    plotter = plt.SudokuPlot(N)

    print("Initial Sudoku:\n")
    plotter.print_grid(board)

    t_start = time.time()
    result_board = solver.solve(plotter, steps=50)
    t_end = time.time()

    print("Solved sudoku:\n")
    plotter.print_grid(result_board)
    print("\nElapsed time: {} secs".format(t_end - t_start))

    print("\nValid sudoku: ", solver.is_valid(result_board))


if __name__ == "__main__":
    main()
