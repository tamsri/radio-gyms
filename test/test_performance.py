import os
from unittest import TestCase
from time import time
from radio_gyms.engines.ray_tracer.tracer import Tracer
from radio_gyms.utils.constants import MAX_FLT

POZNAN_SCENE_PATH = os.path.join(os.getcwd(), "assets", "models", "poznan.obj")

class TestPerformance(TestCase):
    def test_intersection(self):
        tracer = Tracer(POZNAN_SCENE_PATH)
        tx_pos = [0, 20, 0]
        rx_pos = [-30, 1.5, 45]
        ray = Tracer.make_ray(tx_pos, rx_pos)
        # perform brute force
        brute_force_start = time()
        nearest_hit_bf = MAX_FLT
        for triangle in tracer.triangles:
            res = triangle.is_intersect(ray)
            if res > 0:
                nearest_hit_bf = min(res, nearest_hit_bf)
        brute_force_end = time()
        # perform with bounding box tree
        optimize_start = time()
        nearest_hit_op = tracer.map.is_intersect(ray)
        optimize_end = time()
        print(f'brute force tracing {nearest_hit_bf:0.2f}, {(brute_force_end - brute_force_start)*1000:.2f} ms')
        print(f'optimized tracing {nearest_hit_op:0.2f}, {(optimize_end - optimize_start)*1000:.2f} ms')

    def test_diff_scanning(self):
        pass
