import heapq
from typing import List, Tuple, TypeVar
from itertools import count

T = TypeVar('T')


class PriorityQueue:
    def __init__(self):
        self.id_counter = count()
        self.elements: List[Tuple[float, int, T]] = []

    def empty(self) -> bool:
        return not self.elements

    def put(self, item: T, priority: float):
        heapq.heappush(self.elements, (priority, next(self.id_counter), item))

    def get(self) -> Tuple[float, T]:
        element = heapq.heappop(self.elements)
        return element[0], element[2]
