
from typing import List, Callable, Optional, Tuple
from geometry import Point, Line, Rectangle, rectangle_from_points, AxisType
from draw_tool import Scene, PointsCollection, LinesCollection, Plot


class _Node:
    def __init__(self, points: List[Point], region: Optional[Rectangle] = None, depth: int = 0):
        self.points: List[Point] = points
        self.is_leaf: bool = len(points) == 1

        self.region: Rectangle = region if region is not None else rectangle_from_points(points)

        self.division_axis_type: AxisType = AxisType(depth % 2)
        self.__point_comparing_key: Callable[[Point], float] = \
            (lambda p: p[0]) if self.division_axis_type is AxisType.Y else (lambda p: p[1])

        median = self.__median()
        self.dividing_line: float = median if not self.is_leaf else None

        left_points = list(filter(lambda p: self.__point_comparing_key(p) <= median, points))
        self.left = _Node(
            left_points,
            region=self.region.less_than(median, self.division_axis_type),
            depth=depth + 1
        ) if (not self.is_leaf) and len(left_points) > 0 else None

        right_points = list(filter(lambda p: self.__point_comparing_key(p) > median, points))
        self.right = _Node(
            right_points,
            region=self.region.greater_than(median, self.division_axis_type),
            depth=depth + 1
        ) if (not self.is_leaf) and len(right_points) > 0 else None

    def __median(self) -> float:
        temp = sorted(list(map(self.__point_comparing_key, self.points)))
        if len(temp) % 2 == 1:
            return temp[len(temp) // 2]
        else:
            return (temp[len(temp) // 2] + temp[(len(temp) - 1) // 2]) / 2

    def get_divider_line(self) -> Line:
        if self.division_axis_type is AxisType.X:
            return (self.region.min_x, self.dividing_line), (self.region.max_x, self.dividing_line)
        else:
            return (self.dividing_line, self.region.min_y), (self.dividing_line, self.region.max_y)


def _kd_search(node: _Node, rectangle: Rectangle) -> List[Point]:
    def search_child(child: _Node) -> List[Point]:
        if child.region <= rectangle:
            return child.points
        elif child.region & rectangle is not None:
            return _kd_search(child, rectangle)
        else:
            return []

    if node.is_leaf:
        return node.points if node.region <= rectangle else []
    result = []
    if node.right is not None:
        result.extend(search_child(node.left))
    if node.left is not None:
        result.extend(search_child(node.right))
    return result


def _get_lines_from_subtree(node: _Node) -> Tuple[List[Line], List[Line]]:
    rectangles: List[Line] = node.region.get_lines()
    if node.is_leaf:
        return rectangles, []
    dividers: List[Line] = [node.get_divider_line()]

    def get_from_child(child: _Node):
        if child is not None:
            child_rects, child_divs = _get_lines_from_subtree(child)
            rectangles.extend(child_rects)
            dividers.extend(child_divs)

    get_from_child(node.left)
    get_from_child(node.right)
    return rectangles, dividers


class KDTree:
    def __init__(self, points: List[Point]):
        self.__root: _Node = _Node(points)

    def search(self, x_min: float, x_max: float, y_min: float, y_max: float) -> List[Point]:
        rectangle = Rectangle(x_min, x_max, y_min, y_max) & self.__root.region
        return _kd_search(self.__root, rectangle)


if __name__ == "__main__":
    Points: List[Point] = [
        (1, 1),
        (1, 2),
        (1, 3),
        (2, 1),
        (2, 2),
        (2, 3),
        (3, 1),
        (3, 2),
        (3, 3)
    ]

    Tree = KDTree(Points)
    print(Points)
    print(Tree.search(0, 1, 0, 1))
