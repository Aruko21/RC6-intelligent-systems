import numpy as np
import plotter as sudoku_plt
from board import SudokuBoard
import queue
from itertools import count

unique = count()


# Алгоритм - поиск от наилучшего
class SudokuSolver:
    def __init__(self, base_sudoku):
        self.queue = queue.PriorityQueue()
        base_board = SudokuBoard(base_sudoku)

        if not self.is_valid(base_board):
            raise ValueError("Invalid sudoku!")

        self.queue.put((self.fitness_func(base_board), next(unique), base_board))

    @staticmethod
    def fitness_func(sudoku_board):
        empty_cells = 0

        for row_i in range(0, sudoku_board.dim):
            for col_i in range(0, sudoku_board.dim):
                value = sudoku_board.grid[row_i, col_i]
                if value == 0:
                    empty_cells += 1

        return empty_cells

    @staticmethod
    def get_candidate_values_for_cell(sudoku_board, row_i, col_i):
        # Варианты значений для ячейки кодируются bool-массивом
        candidate_values = np.full(16, True, dtype=bool)

        # поиск по столбцу
        for tmp_row_i in range(0, sudoku_board.dim):
            if tmp_row_i != row_i:
                value = sudoku_board.grid[tmp_row_i, col_i]
                if value > 0:
                    candidate_values[value - 1] = False

        # поиск по строке
        for tmp_col_i in range(0, sudoku_board.dim):
            if tmp_col_i != col_i:
                value = sudoku_board.grid[row_i, tmp_col_i]
                if value > 0:
                    candidate_values[value - 1] = False

        square_row_i, square_col_i = sudoku_board.get_square_i(row_i, col_i)
        # поиск по квадрату
        for tmp_row_i in range(square_row_i * sudoku_board.base, (square_row_i + 1) * sudoku_board.base):
            for tmp_col_i in range(square_col_i * sudoku_board.base, (square_col_i + 1) * sudoku_board.base):
                if tmp_row_i != row_i and tmp_col_i != col_i:
                    value = sudoku_board.grid[tmp_row_i, tmp_col_i]
                    if value > 0:
                        candidate_values[value - 1] = False

        return candidate_values

    @staticmethod
    def get_len_of_candidate_values(candidate_values):
        count = 0

        for mask in candidate_values:
            if mask:
                count += 1

        return count

    @staticmethod
    def get_most_constrained_cell(sudoku_board):
        result_row_i = 0
        result_col_i = 0

        min_length = 16
        min_candidates = []

        for row_i in range(0, sudoku_board.dim):
            for col_i in range(0, sudoku_board.dim):
                if sudoku_board.grid[row_i, col_i] == 0:
                    tmp_candidates = SudokuSolver.get_candidate_values_for_cell(sudoku_board, row_i, col_i)
                    tmp_len = SudokuSolver.get_len_of_candidate_values(tmp_candidates)
                    if tmp_len < min_length:
                        min_length = tmp_len
                        min_candidates = tmp_candidates
                        result_row_i = row_i
                        result_col_i = col_i

        result_candidates = []
        for i in range(0, len(min_candidates)):
            if min_candidates[i]:
                result_candidates.append(i + 1)

        return result_row_i, result_col_i, result_candidates

    @staticmethod
    def is_valid(sudoku_board):
        # Проверка по всем строкам
        for row_i in range(0, sudoku_board.dim):
            tmp_values = np.full(sudoku_board.dim, False, dtype=bool)
            for col_i in range(0, sudoku_board.dim):
                value = sudoku_board.grid[row_i, col_i]
                if value != 0:
                    if tmp_values[value - 1]:
                        return False
                    else:
                        tmp_values[value - 1] = True

        # Проверка по всем столбцам
        for col_i in range(0, sudoku_board.dim):
            tmp_values = np.full(sudoku_board.dim, False, dtype=bool)
            for row_i in range(0, sudoku_board.dim):
                value = sudoku_board.grid[row_i, col_i]
                if value != 0:
                    if tmp_values[value - 1]:
                        return False
                    else:
                        tmp_values[value - 1] = True

        # Проверка по всем квадратам
        for square_row_i in range(0, sudoku_board.base):
            for square_col_i in range(0, sudoku_board.base):
                tmp_values = np.full(sudoku_board.dim, False, dtype=bool)
                for row_i in range(square_row_i * sudoku_board.base, (square_row_i + 1) * sudoku_board.base):
                    for col_i in range(square_col_i * sudoku_board.base, (square_col_i + 1) * sudoku_board.base):
                        value = sudoku_board.grid[row_i, col_i]
                        if value != 0:
                            if tmp_values[value - 1]:
                                return False
                            else:
                                tmp_values[value - 1] = True

        return True

    def solve(self, steps=False):
        result = None

        while not self.queue.empty():
            board_queue_item = self.queue.get()

            board = board_queue_item[2]
            board_fitness = board_queue_item[0]

            if steps:
                print("tmp solution: ")
                plotter = sudoku_plt.SudokuPlot(board.grid, 4)
                plotter.print_grid()
                print("Fitness function: {}\n".format(board_fitness))

            if board_fitness == 0:
                result = board
                break

            best_cell_row, best_cell_col, candidates = SudokuSolver.get_most_constrained_cell(board)

            for candidate_value in candidates:
                tmp_board = SudokuBoard(board.grid)
                tmp_board.grid[best_cell_row, best_cell_col] = candidate_value
                fitness = self.fitness_func(tmp_board)
                self.queue.put((fitness, next(unique), tmp_board))

        if result is None:
            raise ValueError("Unable to solve sudoku")

        if not self.is_valid(result):
            raise ValueError("Invalid result sudoku")

        return result.grid
