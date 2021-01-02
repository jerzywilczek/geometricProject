from typing import List, Callable, Optional, Tuple, Union
from geometry import Point, Line, Rectangle, rectangle_from_points, AxisType
from draw_tool import Scene, PointsCollection, LinesCollection

VisualizingFrame = Tuple[List[Point], List[Line]]
_COLOR_SEARCHED_RECT = "black"
_COLOR_CONSIDERED_NOW = "red"
_COLOR_FOUND_POINT = "red"
_COLOR_DIVIDER = "yellow"


class _Node:
    def __init__(self, points: List[Point], region: Optional[Rectangle] = None, depth: int = 0):
        self.points: List[Point] = points
        self.is_leaf: bool = len(points) == 1

        self.region: Rectangle = region if region is not None else rectangle_from_points(points)

        x_coords = list(map(lambda p: p[0], points))
        x_diff = max(x_coords) - min(x_coords)
        y_coords = list(map(lambda p: p[1], points))
        y_diff = max(y_coords) - min(y_coords)
        self.division_axis_type: AxisType = AxisType.Y if x_diff >= y_diff else AxisType.X
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

    def get_lines_from_node(self) -> Tuple[List[Line], List[Line]]:
        rectangle: List[Line] = self.region.get_lines() if self.region is not None else []
        if self.is_leaf:
            return rectangle, []
        return rectangle, [self.get_divider_line()]


def _kd_search(node: _Node, rectangle: Rectangle, frames: Optional[List[VisualizingFrame]] = None) -> List[Point]:
    if node.is_leaf:
        if rectangle.point_inside(node.points[0]):
            if frames is not None:
                frames.append((node.points, node.get_lines_from_node()[0]))
            return node.points
        else:
            if frames is not None:
                frames.append(([], node.get_lines_from_node()[0]))
            return []
    result = []

    if frames is not None:
        frames.append(([], node.get_lines_from_node()[0]))

    def search_child(child: _Node) -> List[Point]:
        if child.region <= rectangle:
            if frames is not None:
                frames.append((child.points, child.get_lines_from_node()[0]))
            return child.points
        elif child.region & rectangle is not None:
            return _kd_search(child, rectangle, frames=frames)
        else:
            return []

    if node.right is not None:
        result.extend(search_child(node.left))
    if node.left is not None:
        result.extend(search_child(node.right))
    if frames is not None:
        frames.append((result, node.get_lines_from_node()[0]))
    return result


def _get_lines_from_subtree(node: _Node) -> Tuple[List[Line], List[Line]]:
    rectangles, dividers = node.get_lines_from_node()

    def get_from_child(child: _Node):
        if child is not None:
            child_rects, child_divs = _get_lines_from_subtree(child)
            rectangles.extend(child_rects)
            dividers.extend(child_divs)

    if node is not None:
        get_from_child(node.left)
        get_from_child(node.right)
    return rectangles, dividers


class KDTree:
    def __init__(self, points: List[Point]):
        self.__root: _Node = _Node(points)
        self.__rectangles, self.__dividers = _get_lines_from_subtree(self.__root)

    def search(self, x_min: float, x_max: float, y_min: float, y_max: float, visualize: bool = False) \
            -> Union[List[Point], Tuple[List[Point], List[Scene]]]:
        rectangle = Rectangle(x_min, x_max, y_min, y_max) & self.__root.region
        if not visualize:
            return _kd_search(self.__root, rectangle)

        frames: List[VisualizingFrame] = []
        points = _kd_search(self.__root, rectangle, frames=frames)
        scenes: List[Scene] = [self.get_visualized()]

        def scene_from_frame(frame: VisualizingFrame) -> Scene:
            vis_points, vis_lines = frame
            return Scene(
                points=[
                    PointsCollection(self.__root.points),
                    PointsCollection(vis_points, color=_COLOR_FOUND_POINT)
                ],
                lines=[
                    LinesCollection(self.__rectangles),
                    LinesCollection(self.__dividers, color=_COLOR_DIVIDER),
                    LinesCollection(rectangle.get_lines(), color=_COLOR_SEARCHED_RECT),
                    LinesCollection(vis_lines, color=_COLOR_CONSIDERED_NOW)
                ]
            )

        scenes.extend(map(scene_from_frame, frames))
        return points, scenes

    def get_visualized(self) -> Scene:
        return Scene(
            points=[
                PointsCollection(self.__root.points)
            ],
            lines=[
                LinesCollection(self.__rectangles),
                LinesCollection(self.__dividers, color=_COLOR_DIVIDER),
            ]
        )


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
    print(Tree.search(1, 4, 1, 4))
