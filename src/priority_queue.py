class PriorityQueue:
    def __init__(self) -> None:
        self.elements: list[tuple[int, tuple[int, int]]] = []

    def empty(self) -> bool:
        return len(self.elements) == 0

    def push(self, priority: int, item: tuple[int, int]) -> None:
        self.elements.append((priority, item))

    def pop(self) -> tuple[int, int] | None:
        if self.empty():
            return None
        min_index_so_far: int = 0
        for i, tuple in enumerate(self.elements):
            if tuple[0] < self.elements[min_index_so_far][0]:
                min_index_so_far = i
        item = self.elements[min_index_so_far][1]
        del self.elements[min_index_so_far]
        return item

    def priority(self, i: int) -> int:
        return self.elements[i][0]
