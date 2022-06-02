import numpy as np
from typing import List, Tuple


class Block:
    def __init__(self, *coords_with_labels):
        self.size = len(coords_with_labels)
        self.coords = []
        self.labels = []

        is_horizontal = False
        sorted_coords_with_labels = coords_with_labels
        if len(coords_with_labels) > 1:
            is_horizontal = coords_with_labels[0][0] == coords_with_labels[1][0]

            sorted_coords_with_labels = sorted(coords_with_labels, key=lambda coord: coord[int(is_horizontal)])

        self.coords = list(map(lambda item: [item[0], item[1]], sorted_coords_with_labels))
        self.labels = list(map(lambda item: item[2], sorted_coords_with_labels))


class Board:
    def __init__(self, x_size, y_size):
        self.board = np.empty((y_size, x_size), dtype=Block)

    def __hash__(self):
        # Хэш - функция от tuple, в начале которого координаты пустых ячеек, а затем перечисление всех блоков (фишек)
        empty_cells = self.get_empty_cells()
        all_blocks = self.get_all_blocks()
        all_blocks_tuple = []
        for block in all_blocks:
            coords_list = []
            for coord in coords_list:
                coords_list.append(tuple(coord))

            all_blocks_tuple.append((tuple(coords_list), tuple(block.labels)))

        to_hash = (tuple(empty_cells), tuple(all_blocks_tuple))
        return hash(to_hash)

    def __eq__(self, other):
        # для операций if item in list/dict
        return self.__hash__() == other.__hash__()

    def set_blocks(self, blocks):
        for block in blocks:
            self.set_block(block)

    def set_block(self, block):
        if self.can_place(block.coords):
            for coord in block.coords:
                self.board[coord[0], coord[1]] = block

    def pop_block(self, coord) -> Block:
        block = self.get_block_by_pos(*coord)

        for coord in block.coords:
            self.board[coord[0], coord[1]] = None

        return block

    def can_place(self, coords) -> bool:
        for coord in coords:
            try:
                if not self.board[coord[0], coord[1]] is None:
                    return False
            except IndexError:
                # Если для блока не хватает места на поле
                return False

        return True

    def get_new_coords_for_move(self, block_coord, move_coord) -> List[List[int]]:
        block = self.get_block_by_pos(block_coord[0], block_coord[1])

        move_x = 0
        move_y = 0

        anchor_coord = block_coord

        if len(block.coords) > 1:
            if anchor_coord[0] != move_coord[0] and anchor_coord[1] != move_coord[1]:
                # NOTE: В рамках упрощения рассматриваем то, что блок может быть только в 2 клетки
                # для масштабирования надо сделать цикл поиска
                if tuple(anchor_coord) == tuple(block.coords[0]):
                    anchor_coord = block.coords[1]
                else:
                    anchor_coord = block.coords[0]

                if anchor_coord[0] != move_coord[0] and anchor_coord[1] != move_coord[1]:
                    # Подобное также является упрощением, так как знаем, что свободно только 2 фишки.
                    # А значит никак не можем двигать блоки из 2 ячеек по диагонали
                    raise ValueError("Invalid move")

        move_x = move_coord[1] - anchor_coord[1]
        move_y = move_coord[0] - anchor_coord[0]

        # copy old coords
        new_coords = []
        for coord in block.coords:
            new_coords.append(list(coord[:]))

        for i in range(len(new_coords)):
            new_coords[i][0] += move_y
            new_coords[i][1] += move_x

        return new_coords

    def can_move(self, block_coord, move_coord) -> bool:
        block = self.get_block_by_pos(block_coord[0], block_coord[1])

        try:
            new_coords = self.get_new_coords_for_move(block_coord, move_coord)
        except ValueError:
            # Если пытаемся выполнить невозможный переход
            return False

        self.pop_block(block_coord)
        result = self.can_place(new_coords)
        self.set_block(block)

        return result

    def move_block(self, block_coord, move_coord) -> bool:
        block = self.get_block_by_pos(block_coord[0], block_coord[1])

        if self.can_move(block_coord, move_coord):
            new_coords = self.get_new_coords_for_move(block_coord, move_coord)
            self.pop_block(block_coord)
            block.coords = new_coords
            self.set_block(block)
            return True
        else:
            return False

    def get_block_by_pos(self, y, x) -> Block:
        return self.board[y, x]

    def get_label_by_pos(self, y, x) -> str:
        block = self.get_block_by_pos(y, x)

        label = None
        if block is not None:
            coord_index = block.coords.index([y, x])
            label = block.labels[coord_index]

        return label

    def get_all_blocks(self) -> List[Block]:
        blocks = []
        for i in range(self.board.shape[0]):
            for j in range(self.board.shape[1]):
                block = self.get_block_by_pos(i, j)
                if block is not None and block not in blocks:
                    blocks.append(block)

        return blocks

    def get_empty_cells(self) -> List[Tuple[int, int]]:
        cells = []
        for i in range(self.board.shape[0]):
            for j in range(self.board.shape[1]):
                block = self.get_block_by_pos(i, j)
                if block is None:
                    cells.append((i, j))

        return cells

    def get_possible_moves(self) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        moves = []

        for i in range(self.board.shape[0]):
            for j in range(self.board.shape[1]):
                free_blocks = self.get_free_blocks(i, j)
                if len(free_blocks) > 0:
                    for block_coord in free_blocks:
                        move = (block_coord, (i, j))
                        if move not in moves:
                            if self.can_move(block_coord, (i, j)):
                                moves.append(move)

        return moves

    def get_free_blocks(self, y, x, except_direction=None) -> List[Tuple[int, int]]:
        # Фишки, которые прилегают к клетке с координатами (y, x)
        free_blocks = []

        target_block = self.get_block_by_pos(y, x)

        if target_block is None:
            # сверху
            if y > 0 and except_direction != "up":
                test_coord = (y - 1, x)
                potential_block = self.get_block_by_pos(*test_coord)
                if potential_block is not None:
                    if test_coord not in free_blocks:
                        free_blocks.append(test_coord)
                else:
                    free_blocks += self.get_free_blocks(*test_coord, except_direction="down")

            # справа
            if x < self.board.shape[1] - 1 and except_direction != "right":
                test_coord = (y, x + 1)
                potential_block = self.get_block_by_pos(*test_coord)
                if potential_block is not None:
                    if test_coord not in free_blocks:
                        free_blocks.append(test_coord)
                else:
                    free_blocks += self.get_free_blocks(*test_coord, except_direction="left")

            # снизу
            if y < self.board.shape[0] - 1 and except_direction != "down":
                test_coord = (y + 1, x)
                potential_block = self.get_block_by_pos(*test_coord)
                if potential_block is not None:
                    if test_coord not in free_blocks:
                        free_blocks.append(test_coord)
                else:
                    free_blocks += self.get_free_blocks(*test_coord, except_direction="up")

            # слева
            if x > 0 and except_direction != "left":
                test_coord = (y, x - 1)
                potential_block = self.get_block_by_pos(*test_coord)
                if potential_block is not None:
                    if test_coord not in free_blocks:
                        free_blocks.append(test_coord)
                else:
                    free_blocks += self.get_free_blocks(*test_coord, except_direction="right")

        return free_blocks
