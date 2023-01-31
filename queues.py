import math
from heapq import heappop, heappush
from typing import List, Tuple
from task import Task


class TaskQueue:
    def __init__(self):
        self._elements: List[Task] = []
        self.rrt = math.inf

    def dequeue(self) -> Task:
        return self._elements.pop()

    def __len__(self):
        return len(self._elements)


class FifoQueue(TaskQueue):
    def enqueue(self, value: Task):
        self._elements.append(value)
        value.current_queue = self


class RoundRobinQueue(FifoQueue):
    def __init__(self, rrt: int):
        super().__init__()
        self.rrt = rrt


class PriorityQueue:
    def __init__(self):
        self._elements: List[Tuple[int, Task]] = []

    def enqueue_with_priority(self, priority: int, value: Task):
        heappush(self._elements, (-priority, value))
        value.current_queue = self

    def dequeue(self):
        return heappop(self._elements)[1]

    def __len__(self):
        return len(self._elements)
