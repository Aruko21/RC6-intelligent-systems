import threading
import queue
from typing import List

import board as brd


START_X = 60
START_Y = 60


class BoardWindow(threading.Thread):
    def __init__(self, cell_size: int, max_width: int, max_height: int, framerate: int):
        self.call_queue = queue.Queue()
        self.call_timeout = 1.0 / framerate

        self.cell_size: int = cell_size
        self.max_width: int = max_width
        self.max_height: int = max_height

        self.frontend = None
        self.screen = None
        self.font = None

        self.quit = False

        super(BoardWindow, self).__init__()

    # Метод проксирования вызовов из MainThread в UI Thread
    def call_ui(self, function, *args, **kwargs):
        self.call_queue.put((function, args, kwargs))

    def run(self):
        # pygame должен импортироваться в конкретном потоке, т.к. сам по себе не является потокобезопасным
        import pygame
        self.frontend = pygame

        self.init()

        while not self.quit:
            try:
                # Задержка для обеспечения нужного FPS осуществлена путем ожидания элемента в очереди вызовов
                function, args, kwargs = self.call_queue.get(timeout=self.call_timeout)
                function(*args, **kwargs)
            except queue.Empty:
                self.event_loop()

        self.frontend.quit()

    def init(self):
        self.frontend.init()
        # Используется шрифт для отображения UTF-8 символов (звездочка)
        self.font = self.frontend.font.SysFont("segoeuisymbol", 50)

        self.screen = self.frontend.display.set_mode((600, 500))
        self.frontend.display.set_caption("Stars")

        self.clear()

    def clear(self):
        border_width = 2

        self.screen.fill(self.frontend.color.THECOLORS["azure1"])
        self.frontend.draw.rect(self.screen, self.frontend.color.THECOLORS["azure2"],
                                self.frontend.Rect(START_X, START_Y, self.cell_size * self.max_width,
                                                   self.cell_size * self.max_height))
        self.frontend.draw.rect(self.screen, self.frontend.color.THECOLORS["azure4"],
                                self.frontend.Rect(START_X - 2, START_Y - 2, self.cell_size * self.max_width + 4,
                                                   self.cell_size * self.max_height + 4), width=border_width)

    def event_loop(self):
        for event in self.frontend.event.get():
            if event.type == self.frontend.QUIT:
                self.quit = True

        # Перерисовать весь экран
        self.frontend.display.flip()

    def draw_board(self, board: brd.Board):
        self.call_ui(self._draw_board, board)

    def _draw_board(self, board: brd.Board):
        self.clear()

        all_blocks: List[brd.Block] = board.get_all_blocks()

        for block in all_blocks:
            # рассматриваем только прямоугольники (по контракту)
            board_x = block.coords[0][1]
            board_y = block.coords[0][0]
            cells_x = 1
            cells_y = 1

            if len(block.coords) > 1:
                if block.coords[0][0] == block.coords[1][0]:
                    cells_x = len(block.coords)
                else:
                    cells_y = len(block.coords)

            block_x = START_X + board_x * self.cell_size
            block_y = START_Y + board_y * self.cell_size
            block_width = self.cell_size * cells_x
            block_height = self.cell_size * cells_y

            block_rect = self.frontend.Rect(block_x, block_y, block_width, block_height)
            self.frontend.draw.rect(self.screen, self.frontend.color.THECOLORS["aliceblue"], block_rect)
            self.frontend.draw.rect(self.screen, self.frontend.color.THECOLORS["azure3"], block_rect, width=1)

            if len(block.labels) > 1 and block.labels[0] == block.labels[1] and block.labels[0] != "*":
                # Если у всего блока одинаковый label и это не звездочка, то отобразить его по центру всего блока
                text_title = self.font.render(block.labels[0], True, self.frontend.color.THECOLORS["azure4"])
                rect_title = text_title.get_rect(center=block_rect.center)
                self.screen.blit(text_title, rect_title)
            else:
                # Иначе заполнение текстовых меток блоков для каждой отдельной ячейки
                for i in range(len(block.labels)):
                    text = block.labels[i]
                    if text == "*":
                        text = "☆"

                    text_rect_x = block_rect.x
                    text_rect_y = block_rect.y
                    text_rect_width = block_width
                    text_rect_height = block_height

                    if cells_x > 1:
                        text_rect_x += i * self.cell_size
                        text_rect_width //= len(block.labels)
                    else:
                        text_rect_y += i * self.cell_size
                        text_rect_height //= len(block.labels)

                    text_rect = self.frontend.Rect(text_rect_x, text_rect_y, text_rect_height, text_rect_width)

                    text_title = self.font.render(text, True, self.frontend.color.THECOLORS["azure4"])
                    rect_title = text_title.get_rect(center=text_rect.center)
                    self.screen.blit(text_title, rect_title)
