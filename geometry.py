from __future__ import annotations

from enum import Enum, unique
from typing import Tuple, List, Optional

Point = Tuple[float, float]


@unique
class AxisType(Enum):
    X = 0
    Y = 1


class Rectangle:
    def __init__(self, min_x: float, max_x: float, min_y: float, max_y: float):
        self.min_x: float = min_x
        self.max_x: float = max_x
        self.min_y: float = min_y
        self.max_y: float = max_y

    def less_than(self, line: float, axis: AxisType) -> Optional[Rectangle]:
        if axis is AxisType.X:
            if self.max_x < line:
                return self
            if self.min_x > line:
                return None
            return Rectangle(self.min_x, line, self.min_y, self.max_y)
        else:
            if self.max_y < line:
                return self
            if self.min_y > line:
                return None
            return Rectangle(self.min_x, self.max_x, self.min_y, line)

    def greater_than(self, line: float, axis: AxisType):
        if axis is AxisType.X:
            if self.min_x > line:
                return self
            if self.max_x < line:
                return None
            return Rectangle(line, self.max_x, self.min_y, self.max_y)
        else:
            if self.min_y > line:
                return self
            if self.max_y < line:
                return None
            return Rectangle(self.min_x, self.max_x, line, self.max_y)


def rectangle_from_points(points: List[Point]) -> Optional[Rectangle]:
    x_coords = list(map(lambda p: p[0], points))
    y_coords = list(map(lambda p: p[1], points))
    min_x = min(x_coords)
    max_x = max(x_coords)
    min_y = min(y_coords)
    max_y = max(y_coords)
    return Rectangle(min_x, max_x, min_y, max_y) if min_x != max_x and min_y != max_y else None
