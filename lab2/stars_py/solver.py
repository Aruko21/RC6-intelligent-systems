import utils as utl
import board as brd
from copy import deepcopy

import time

from typing import Dict, List, Tuple, Optional


# Решатель головоломки алгоритмом A*
class Solver:
    def __init__(self, board: brd.Board):
        self.base_board: brd.Board = board
        self.queue = utl.PriorityQueue()

    @staticmethod
    def get_heuristic(board):
        summ = 0

        # Количество звездочек не на своем месте по горизонтали
        for i in range(board.board.shape[0]):
            # Среднюю линию не учитываем
            if i == 1:
                continue
            for j in range(board.board.shape[1]):
                if board.get_label_by_pos(i, j) == "*":
                    summ += 1

        # Количество звездочек не на своем месте по вертикали
        for j in range(board.board.shape[1]):
            stars_count = 0
            for i in range(board.board.shape[0]):
                if board.get_label_by_pos(i, j) == "*":
                    stars_count += 1
            if stars_count > 1:
                summ += stars_count - 1

        return summ

    @staticmethod
    def get_possible_states(board) -> List[brd.Board]:
        states = []

        moves = board.get_possible_moves()

        for move in moves:
            new_state = deepcopy(board)
            new_state.move_block(move[0], move[1])
            states.append(new_state)

        return states

    def solve(self, printer) -> Tuple[List[brd.Board], int]:
        self.queue.put(self.base_board, Solver.get_heuristic(self.base_board))

        came_from: Dict[brd.Board, Optional[brd.Board]] = {
            self.base_board: None
        }
        moves_num: Dict[brd.Board, int] = {
            self.base_board: 0
        }

        while not self.queue.empty():
            current_state: Tuple[float, brd.Board] = self.queue.get()
            current_cost = current_state[0]
            current_board = current_state[1]

            # time.sleep(0.5)
            # printer.draw_board(current_board)
            print("current heuristic: ", current_cost - moves_num[current_board])
            if current_cost - moves_num[current_board] == 0:
                # Найдено решение
                return self.reconstruct_best_solution(current_board, came_from), moves_num[current_board]

            for new_board in Solver.get_possible_states(current_board):
                new_cost = moves_num[current_board] + 1
                if new_board not in moves_num or new_cost < moves_num[new_board]:
                    moves_num[new_board] = new_cost
                    priority = new_cost + self.get_heuristic(new_board)

                    # printer.draw_board(new_board)
                    # print("new heuristic: ", priority - new_cost)

                    self.queue.put(new_board, priority)
                    came_from[new_board] = current_board

        raise ValueError("No solution!")

    def reconstruct_best_solution(self, goal, came_from) -> List[brd.Board]:
        solution = [goal]
        step_state = goal

        while step_state != self.base_board:
            step_state = came_from[step_state]
            solution.append(step_state)

        solution.reverse()
        return solution
