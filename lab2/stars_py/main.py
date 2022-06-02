import time
import copy

import board as brd
import solver as slv
import graphics as graph

CELL_SIZE = 90
BOARD_WIDTH = 5
BOARD_HEIGHT = 3

FRAMERATE = 60


def main():
    blocks = [
        brd.Block((1, 0, "4"), (2, 0, "*")),
        brd.Block((0, 1, "1")),
        brd.Block((1, 1, "5")),
        brd.Block((2, 1, "*")),
        brd.Block((0, 2, "*"), (1, 2, "2")),
        brd.Block((2, 2, "8")),
        brd.Block((0, 3, "*"), (0, 4, "*")),
        brd.Block((1, 3, "6"), (1, 4, "6")),
        brd.Block((2, 3, "9"))
    ]

    board = brd.Board(x_size=BOARD_WIDTH, y_size=BOARD_HEIGHT)
    board.set_blocks(blocks)

    graphics = graph.BoardWindow(cell_size=CELL_SIZE, max_width=BOARD_WIDTH, max_height=BOARD_HEIGHT, framerate=FRAMERATE)
    graphics.start()

    solver = slv.Solver(board)

    graphics.draw_board(board)
    time.sleep(0.5)

    start_time = time.time()
    solution, moves = solver.solve(graphics)
    exec_time = time.time() - start_time

    print("Execution time: %f secs" % exec_time)
    print("Number of moves: ", moves)

    for step in solution:
        graphics.draw_board(step)
        time.sleep(0.5)

    graphics.draw_board(solution[-1])

    # Вызов функции обязателен, иначе прога закроется сразу после решения
    graphics.join()


if __name__ == "__main__":
    main()
