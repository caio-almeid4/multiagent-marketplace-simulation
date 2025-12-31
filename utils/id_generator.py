from itertools import count


class SerialIDGenerator:
    def __init__(self, start: int = 1):
        self._counter = count(start)

    def generate(self) -> int:
        return next(self._counter)
