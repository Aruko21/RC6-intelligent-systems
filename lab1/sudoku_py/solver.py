import numpy as np
import plotter as sudoku_plt
import copy
import random
from board import SudokuBoard
from typing import List, Tuple, TypeVar, Optional



# Алгоритм - поиск с запретами по полным состояниям(Tabu search)
class SudokuSolver:
    def __init__(self, base_board: SudokuBoard):
        self.tabu_list = []

        self.base_board = base_board
        self.base = self.base_board.base
        self.dim = self.base_board.dim

        # if not self.is_valid(base_board):
        #     raise ValueError("Invalid sudoku!")

    def fitness_func(self, sudoku_board):
        error_sum = 0

        for row_i in range(0, self.dim):
            row_values = [i for i in range(1, self.dim + 1)]

            for col_i in range(0, self.dim):
                value = sudoku_board.grid[row_i, col_i]
                if value in row_values:
                    row_values.remove(value)

            error_sum += len(row_values)

        for col_i in range(0, self.dim):
            col_values = [i for i in range(1, self.dim + 1)]

            for row_i in range(0, self.dim):
                value = sudoku_board.grid[row_i, col_i]
                if value in col_values:
                    col_values.remove(value)

            error_sum += len(col_values)

        return error_sum

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

    @staticmethod
    def fill_random(board) -> SudokuBoard:
        filled_board = copy.deepcopy(board)

        # Заполнение произодится по квадратам
        for square_row_i in range(0, filled_board.base):
            for square_col_i in range(0, filled_board.base):
                values = [i for i in range(1, 17)]
                random.shuffle(values)
                used_values = np.full(filled_board.dim, False, dtype=bool)

                for row_i in range(square_row_i * filled_board.base, (square_row_i + 1) * filled_board.base):
                    for col_i in range(square_col_i * filled_board.base, (square_col_i + 1) * filled_board.base):
                        value = filled_board.grid[row_i, col_i]
                        if value != 0:
                            used_values[value - 1] = True

                value_i = 0
                for row_i in range(square_row_i * filled_board.base, (square_row_i + 1) * filled_board.base):
                    for col_i in range(square_col_i * filled_board.base, (square_col_i + 1) * filled_board.base):
                        if filled_board.grid[row_i, col_i] == 0:
                            while used_values[values[value_i] - 1] == True:
                                value_i += 1
                            filled_board.grid[row_i, col_i] = values[value_i]
                            used_values[values[value_i] - 1] = True
                            value_i += 1

        return filled_board

    @staticmethod
    def if_col_valid(board, col_ind):
        used_values = np.full(board.dim, False, dtype=bool)
        for row_i in range(0, board.dim):
            value = board.grid[row_i, col_ind]
            if used_values[value - 1] != True:
                used_values[value - 1] = True
            else:
                return False
        return True

    @staticmethod
    def if_row_valid(board, row_ind):
        used_values = np.full(board.dim, False, dtype=bool)
        for col_i in range(0, board.dim):
            value = board.grid[row_ind, col_i]
            if used_values[value - 1] != True:
                used_values[value - 1] = True
            else:
                return False
        return True

    def generate_neighbour(self, board: SudokuBoard, max_replacements=None) -> SudokuBoard:
        new_board: SudokuBoard = SudokuBoard(board.grid)

        replacements = self.dim
        if max_replacements is not None:
            replacements = max_replacements

        square_indexes = [i for i in range(0, self.dim)]
        random.shuffle(square_indexes)

        squares_number = random.randint(1, replacements)
        square_indexes = square_indexes[:squares_number]

        for square_ind in square_indexes:
            proper_indexes = False

            square_i = square_ind // self.base
            square_j = square_ind % self.base

            while not proper_indexes:
            # rand_cell_i = random.randint(0, self.base - 1)
            # rand_cell_j = random.randint(0, self.base - 1)

                rand_row1 = random.randint(0, self.base - 1)
                rand_row2 = random.randint(0, self.base - 1)

                rand_col1 = random.randint(0, self.base - 1)
                rand_col2 = random.randint(0, self.base - 1)

                value1_base = self.base_board.grid[square_i * self.base + rand_row1, square_j * self.base + rand_col1]
                value2_base = self.base_board.grid[square_i * self.base + rand_row2, square_j * self.base + rand_col2]

                if (rand_row1 != rand_row2 and rand_col1 != rand_col2) and (value1_base == 0) and (value2_base == 0):
                    proper_indexes = True

            # swap
            tmp = new_board.grid[square_i * self.base + rand_row1, square_j * self.base + rand_col1]
            new_board.grid[square_i * self.base + rand_row1, square_j * self.base + rand_col1] = new_board.grid[square_i * self.base + rand_row2, square_j * self.base + rand_col2]
            new_board.grid[square_i * self.base + rand_row2, square_j * self.base + rand_col2] = tmp

        return new_board

    def solve(self, plotter, steps=False):
        TABU_LEN = 3000
        NEIGHBOURS = 10

        best_board = SudokuSolver.fill_random(self.base_board)
        best_fitness = self.fitness_func(best_board)

        replacements_num = 1
        iterations = 0

        while best_fitness != 0:
            # if steps and iterations % steps == 0:
            print("Iteration #%d. Fitness: %d" % (iterations, best_fitness))

            # if best_fitness < 100:
            #     if best_fitness > 30:
            #         replacements_num = (best_fitness - 30) // float(70 / 16)
            # print("check replacements: ", replacements_num)
            neighbours: List[Tuple[SudokuBoard, int]] = []
            for k in range(0, NEIGHBOURS):
                tmp_board = self.generate_neighbour(best_board, replacements_num)

                if tmp_board not in self.tabu_list:
                    fitness = self.fitness_func(tmp_board)
                    if fitness == 0:
                        return tmp_board
                    neighbours.append((tmp_board, fitness))

            best_tmp_board_item = min(neighbours, key=lambda item: item[1])
            best_tmp_board = best_tmp_board_item[0]
            minimum_err = best_tmp_board_item[1]

            if minimum_err < best_fitness:
                best_board = best_tmp_board
                best_fitness = minimum_err

            if len(self.tabu_list) >= TABU_LEN:
                self.tabu_list.pop(0)
            self.tabu_list.append(best_tmp_board)

            iterations += 1

        return best_board
