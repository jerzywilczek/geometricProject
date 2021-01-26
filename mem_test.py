import sys
import tracemalloc
from typing import Callable
from kd_tree import KDTree
from quadtree import Quadtree
from gen_data import *


def test_kd_buildup(points: List[Point]) -> float:
    tracemalloc.start()
    starting_mem, _ = tracemalloc.get_traced_memory()
    tree = KDTree(points)
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return peak - starting_mem


def test_quadtree_buildup(points: List[Point]) -> float:
    tracemalloc.start()
    starting_mem, _ = tracemalloc.get_traced_memory()
    tree = Quadtree(points)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return peak - starting_mem


class Tester:
    def __init__(self, n_values: List[int], averaging_iterations: int, scope: Tuple[float, float] = (0, 100)):
        self.n_values: List[int] = n_values
        self.test_points: List[List[List[Point]]] = list(map(
            lambda n: [gen_points(scope=scope, n=n) for _ in range(averaging_iterations)],
            self.n_values
        ))

    def print_tests_csv(
            self,
            buildup_tester: Callable[[List[Point]], float],
            filename: str
    ):
        buildup_results: List[float] = []
        total_amount = len(self.n_values) * len(self.test_points[0])
        for i in range(len(self.test_points)):
            result = []
            for j in range(len(self.test_points[0])):
                sys.stdout.write("\rTest {}/{}".format(i * len(self.test_points[0]) + j + 1, total_amount))
                sys.stdout.flush()
                result.append(buildup_tester(self.test_points[i][j]))
            buildup_results.append(sum(result)/len(self.test_points[0]))

        with open(filename + '_buildup_memtest.csv', 'w') as file:
            file.write('n;memory\n')
            for i in range(len(buildup_results)):
                file.write(str(self.n_values[i]) + ';' + str(buildup_results[i]) + '\n')

    def print_tests_both_trees_csv(self, base_filename: str):
        self.print_tests_csv(test_quadtree_buildup, base_filename + '_quadtree')
        self.print_tests_csv(test_kd_buildup, base_filename + '_kd_tree')


class TesterCluster(Tester):
    def __init__(
            self, n_values: List[int],
            averaging_iterations: int,
            scope: Tuple[float, float] = (0, 100),
            cluster_amount: int = 5,
            cluster_radius: float = 5
    ):
        super().__init__(n_values, 0)
        self.test_points = list(map(
            lambda n: [
                gen_point_clusters(
                    scope=scope,
                    points_per_cluster=n//cluster_amount,
                    cluster_amount=cluster_amount,
                    cluster_radius=cluster_radius
                )
                for _ in range(averaging_iterations)],
            self.n_values
        ))


if __name__ == "__main__":
    tester = Tester([10000], 50)
    tester.print_tests_both_trees_csv("dupa")
