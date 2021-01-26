from typing import List, Callable
from geometry import Point, Rectangle
from gen_data import *
from timeit import default_timer
from kd_tree import KDTree
from quadtree import Quadtree


def test_kd_buildup(points: List[Point]) -> float:
    start_time = default_timer()
    _ = KDTree(points)
    end_time = default_timer()
    return end_time - start_time


def test_quadtree_buildup(points: List[Point]) -> float:
    start_time = default_timer()
    _ = Quadtree(points)
    end_time = default_timer()
    return end_time - start_time


def test_kd_search(points: List[Point], rectangles: List[Rectangle]) -> List[float]:
    tree = KDTree(points)

    def time_individual(rectangle: Rectangle) -> float:
        min_x, max_x, min_y, max_y = rectangle.to_tuple()
        start_time = default_timer()
        tree.search(min_x, max_x, min_y, max_y)
        end_time = default_timer()
        return end_time - start_time

    return list(map(time_individual, rectangles))


def test_quadtree_search(points: List[Point], rectangles: List[Rectangle]) -> List[float]:
    tree = Quadtree(points)

    def time_individual(rectangle: Rectangle) -> float:
        start_time = default_timer()
        tree.find(rectangle)
        end_time = default_timer()
        return end_time - start_time

    return list(map(time_individual, rectangles))


class Tester:
    def __init__(self, n_values: List[int], rectangle_amount_per_test: int, scope: Tuple[float, float] = (0, 100)):
        self.n_values: List[int] = n_values
        self.test_points: List[List[Point]] = list(map(lambda n: gen_points(scope=scope, n=n), self.n_values))
        self.test_rectangles: List[List[Rectangle]] = [
            [gen_rect(scope=scope) for _ in range(rectangle_amount_per_test)] for _ in range(len(self.n_values))
        ]

    def print_tests_csv(
            self,
            buildup_tester: Callable[[List[Point]], float],
            search_tester: Callable[[List[Point], List[Rectangle]], List[float]],
            filename: str
    ):
        buildup_results: List[float] = list(map(buildup_tester, self.test_points))
        search_results: List[float] = [
            sum(search_tester(self.test_points[i], self.test_rectangles[i])) / len(self.test_rectangles[0])
            for i in range(len(self.test_points))
        ]
        with open(filename + '_buildup.csv', 'w') as file:
            file.write('n;time\n')
            for i in range(len(buildup_results)):
                file.write(str(self.n_values[i]) + ';' + str(buildup_results[i]) + '\n')
        with open(filename + '_search.csv', 'w') as file:
            file.write('n;mean_time\n')
            for i in range(len(search_results)):
                file.write(str(self.n_values[i]) + ';' + str(search_results[i]) + '\n')

    def print_tests_both_trees_csv(self, base_filename: str):
        self.print_tests_csv(test_quadtree_buildup, test_quadtree_search, base_filename + '_quadtree')
        self.print_tests_csv(test_kd_buildup, test_kd_search, base_filename + '_kd_tree')


class TesterCluster(Tester):
    def __init__(self,
                 n_values: List[int],
                 rectangle_amount_per_test: int,
                 scope: Tuple[float, float] = (0, 100),
                 cluster_amount: int = 5,
                 cluster_radius: float = 5
                 ):
        super().__init__(n_values, rectangle_amount_per_test, scope)
        self.test_points = list(
            map(
                lambda n: gen_point_clusters(
                    scope=scope,
                    points_per_cluster=n//cluster_amount,
                    cluster_amount=cluster_amount,
                    cluster_radius=cluster_radius
                ),
                self.n_values
            )
        )
