import numpy as np
import copy


class SudokuBoard:
    def __init__(self, board):
        self.grid = np.array(copy.deepcopy(board))
        self.base = int(np.sqrt(self.grid.shape[0]))
        self.dim = self.base * self.base

    def __hash__(self):
        tuple_board = []
        for row in self.grid:
            tuple_board.append(tuple(row))

        return hash(tuple(tuple_board))

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def get_square_i(self, row_i, col_i):
        square_row_i = row_i // self.base
        square_col_i = col_i // self.base

        return square_row_i, square_col_i
