from random import uniform
from typing import Tuple, List
from geometry import rectangle_from_points, Rectangle, Point


def gen_points(scope: Tuple[float, float] = (0, 100), n: int = 100):
    return [(uniform(scope[0], scope[1]), uniform(scope[0], scope[1])) for _ in range(n)]


def gen_rect(scope: Tuple[float, float] = (0, 100)) -> Rectangle:
    result = None
    while result is None:
        result = rectangle_from_points([(uniform(scope[0], scope[1]), uniform(scope[0], scope[1])) for _ in range(2)])
    return result


def gen_point_clusters(
        scope: Tuple[float, float] = (0, 100),
        points_per_cluster: int = 100,
        cluster_amount: int = 5,
        cluster_radius: float = 5
) -> List[Point]:
    cluster_centers = [
        (
            uniform(scope[0] + cluster_radius, scope[1] - cluster_radius),
            uniform(scope[0] + cluster_radius, scope[1] - cluster_radius)
        ) for _ in range(cluster_amount)
    ]
    result: List[Point] = []
    for center in cluster_centers:
        result.extend([
            (
                uniform(center[0] - cluster_radius, center[0] + cluster_radius),
                uniform(center[1] - cluster_radius, center[1] + cluster_radius),
            ) for _ in range(points_per_cluster)
        ])
    return result
