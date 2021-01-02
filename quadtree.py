from enum import IntEnum
from typing import List
from draw_tool import *
import copy

from geometry import Point, Rectangle


class Quadrant(IntEnum):
    NE = 0
    NW = 1
    SW = 2
    SE = 3


class _Node:

    def __init__(self, n, s, w, e, quadrant):
        self.boundary = Rectangle(w, e, s, n)
        self.pos = None
        self.max_y = n
        self.min_y = s
        self.min_x = w
        self.max_x = e
        self.mid_y = (self.min_y + self.max_y) / 2
        self.mid_x = (self.min_x + self.max_x) / 2
        self.quadrant = quadrant
        self.children = None

    def add_child(self, node):
        if self.children is None:
            self.children = [None for _ in range(4)]
        self.children[node.quadrant] = node


class Quadtree:

    def __init__(self, points: List[Point]):
        n = max(points, key=lambda p: p[1])[1]
        s = min(points, key=lambda p: p[1])[1]
        w = min(points, key=lambda p: p[0])[0]
        e = max(points, key=lambda p: p[0])[0]
        self.points = points
        self.root = _Node(n, s, w, e, None)
        self.__create_quadtree(self.root, points)

    def __create_quadtree(self, node: _Node, points: List[Point]):
        if len(points) == 1:
            node.pos = points[0]
        if len(points) <= 1:
            return
        ne = _Node(node.max_y, node.mid_y, node.mid_x, node.max_x, Quadrant.NE)
        nw = _Node(node.max_y, node.mid_y, node.min_x, node.mid_x, Quadrant.NW)
        sw = _Node(node.mid_y, node.min_y, node.min_x, node.mid_x, Quadrant.SW)
        se = _Node(node.mid_y, node.min_y, node.mid_x, node.max_x, Quadrant.SE)

        points_ne = [p for p in points if p[0] > node.mid_x and p[1] >= node.mid_y]
        points_nw = [p for p in points if p[0] <= node.mid_x and p[1] > node.mid_y]
        points_sw = [p for p in points if p[0] < node.mid_x and p[1] <= node.mid_y]
        points_se = [p for p in points if p[0] >= node.mid_x and p[1] < node.mid_y]

        node.add_child(ne)
        self.__create_quadtree(ne, points_ne)
        node.add_child(nw)
        self.__create_quadtree(nw, points_nw)
        node.add_child(sw)
        self.__create_quadtree(sw, points_sw)
        node.add_child(se)
        self.__create_quadtree(se, points_se)

    def __find(self, node: _Node, rect: Rectangle, res: List[Point], view):
        if rect.min_x > node.max_x or rect.max_x < node.min_x or rect.min_y > node.max_y or rect.max_y < node.min_y:
            return
        if view is not None:
            view.visited_quadrants.extend(node.boundary.get_lines())
        if node.children is None:
            if node.pos is not None and rect.point_inside(node.pos):
                res.append(node.pos)
                if view is not None:
                    view.points_inside.append(node.pos)
                    view.gen_scene()
            return
        if view is not None:
            view.gen_scene()
        for ch in node.children:
            self.__find(ch, rect, res, view)

    def find(self, rect: Rectangle, visualize=False):
        res = []
        if visualize:
            view = View(self.points, rect, self.root)
            self.__find(self.root, rect, res, view)
            return view.get_plot()
        else:
            self.__find(self.root, rect, res, None)
            return res


class View:

    def __init__(self, points: List[Point], rect: Rectangle, root: _Node):
        self.scenes = []
        self.quadrants = []
        self.visited_quadrants = []
        self.points_inside = []
        self.points = PointsCollection(points)
        self.rect = LinesCollection(lines=rect.get_lines(), color='black')
        self.__gen_quadrants(root)
        self.quadrants = LinesCollection(self.quadrants)
        self.gen_scene()

    def __gen_quadrants(self, node: _Node):
        self.quadrants.extend(node.boundary.get_lines())
        if node.children is not None:
            for ch in node.children:
                if ch is not None:
                    self.__gen_quadrants(ch)

    def gen_scene(self):
        self.scenes.append(Scene(points=[self.points, PointsCollection(copy.deepcopy(self.points_inside), color='red')],
                                 lines=[self.quadrants, self.rect,
                                        LinesCollection(self.visited_quadrants[:-4],
                                                        color='green'),
                                        LinesCollection(self.visited_quadrants[-4:],
                                                        color='red')]))

    def get_plot(self) -> Plot:
        return Plot(scenes=self.scenes)
