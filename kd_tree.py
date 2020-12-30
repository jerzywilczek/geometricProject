from enum import Enum, unique
from typing import List, Callable
from geometry import Point, Rectangle, rectangle_from_points


@unique
class _AxisType(Enum):
    X = 0
    Y = 1


class _Node:
    def __init__(self, points: List[Point], area: Rectangle = None, depth: int = 0):
        self.points: List[Point] = points
        self.is_leaf: bool = len(points) == 1

        self.area = area if area is not None else rectangle_from_points(points)

        self.division_axis_type: _AxisType = _AxisType[depth % 2]
        self.__point_comparing_key: Callable[[Point], float] = \
            (lambda p: p[0]) if self.division_axis_type is _AxisType.Y else (lambda p: p[1])

        median = self.__median()
        self.dividing_line: float = median if not self.is_leaf else None
        self.left = _Node(list(filter(lambda p: self.__point_comparing_key(p) <= median, points)), depth=depth + 1) \
            if not self.is_leaf else None
        self.right = _Node(list(filter(lambda p: self.__point_comparing_key(p) > median, points)), depth=depth + 1) \
            if not self.is_leaf else None

    def __median(self) -> float:
        temp = sorted(list(map(self.__point_comparing_key, self.points)))
        if len(temp) % 2 == 1:
            return temp[len(temp) // 2]
        else:
            return (temp[len(temp) // 2] + temp[(len(temp) - 1) // 2]) / 2
