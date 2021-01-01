from __future__ import annotations

from enum import Enum, unique
from typing import Tuple, List, Optional
from math import inf

Point = Tuple[float, float]
Line = Tuple[Point, Point]


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
        if min_x >= max_x or min_y >= max_y:
            raise ValueError(
                'incorrect parameters for rectangle construction: {}, {}, {}, {}'.format(min_x, max_x, min_y, max_y)
            )

    def __and__(self, other: Rectangle):
        if not isinstance(other, Rectangle):
            return None
        min_x = max(self.min_x, other.min_x)
        max_x = min(self.max_x, other.max_x)
        min_y = max(self.min_y, other.min_y)
        max_y = min(self.max_y, other.max_y)
        if min_x < max_x and min_y < max_y:
            return Rectangle(min_x, max_x, min_y, max_y)
        else:
            return None

    def __eq__(self, other: Rectangle):
        if not isinstance(other, Rectangle):
            return False
        return (
                self.min_x == other.min_x and
                self.max_x == other.max_x and
                self.min_y == other.min_y and
                self.max_y == other.max_y
        )

    def __ne__(self, other: Rectangle):
        if not isinstance(other, Rectangle):
            return False
        return not self == other

    def __le__(self, other: Rectangle):
        if not isinstance(other, Rectangle):
            return False
        return self == self & other

    def __lt__(self, other: Rectangle):
        if not isinstance(other, Rectangle):
            return False
        return self <= other and self != other

    def __ge__(self, other: Rectangle):
        if not isinstance(other, Rectangle):
            return False
        return other == self & other

    def __gt__(self, other: Rectangle):
        if not isinstance(other, Rectangle):
            return False
        return self >= other and self != other

    def less_than(self, line: float, axis: AxisType) -> Optional[Rectangle]:
        if axis is AxisType.X:
            return self & Rectangle(-inf, inf, -inf, line)
        else:
            return self & Rectangle(-inf, line, -inf, inf)

    def greater_than(self, line: float, axis: AxisType) -> Optional[Rectangle]:
        if axis is AxisType.X:
            return self & Rectangle(-inf, inf, line + 10 ** -10, inf)
        else:
            return self & Rectangle(line + 10 ** -10, inf, -inf, inf)

    def point_inside(self, point: Point) -> bool:
        x, y = point
        return self.min_x < x <= self.max_x and self.min_y < y <= self.max_y

    def get_lines(self) -> List[Line]:
        return [
            ((self.min_x, self.min_y), (self.max_x, self.min_y)),
            ((self.max_x, self.min_y), (self.max_x, self.max_y)),
            ((self.max_x, self.max_y), (self.min_x, self.max_y)),
            ((self.min_x, self.max_y), (self.min_x, self.min_y))
        ]


def rectangle_from_points(points: List[Point]) -> Optional[Rectangle]:
    x_coords = list(map(lambda p: p[0], points))
    y_coords = list(map(lambda p: p[1], points))
    min_x = min(x_coords)
    max_x = max(x_coords)
    min_y = min(y_coords)
    max_y = max(y_coords)
    return Rectangle(min_x, max_x, min_y, max_y) if min_x != max_x and min_y != max_y else None
