import unittest
from radio_gyms.engines import Tracer

import os

POZNAN_OBJ_PATH = os.path.join("..", "assets", "models", )

class TestTracer(unittest.TestCase):

    def test_tracer(self):
        tracer = Tracer(POZNAN_OBJ_PATH)
        tx_pos = (0, 15, 0)
        rx_pos = (-30, 1.5, 45)
        result = tracer.traceOutdoor(tx_pos, rx_pos)
        self.assertEqual(result["direct"], False)
        self.assertNotEqual(result["knifeEdges"], [])