from random import uniform
from typing import Tuple
from geometry import rectangle_from_points


def gen_points(scope: Tuple[float, float] = (0, 100), n: int = 100):
    return [(uniform(scope[0], scope[1]), uniform(scope[0], scope[1])) for _ in range(n)]


def gen_rect(scope: Tuple[float, float] = (0, 100)):
    result = None
    while result is None:
        result = rectangle_from_points([(uniform(scope[0], scope[1]), uniform(scope[0], scope[1])) for _ in range(2)])
    return result
