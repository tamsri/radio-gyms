import os
import numpy as np
from unittest import TestCase
from radio_gyms.visualizers import Window
from radio_gyms.engines.ray_tracer.tracer import Tracer
from radio_gyms.utils.converters import outdoor_traced_result_to_line as OutdoorResultToLines

POZNAN_OBJ_PATH = os.path.join(os.getcwd(), "assets", "models", "poznan.obj")

class TestVirtualizer(TestCase):

    def test_result_display(self):
        window = Window()
        tracer = Tracer(POZNAN_OBJ_PATH)
        tx_pos = np.array([0, 5, 0])
        lines = []
        for i in range(1):
            while True:
                rx_pos = (np.random.rand(3)*2-1)*100
                rx_pos[1] = 1.2
                if tracer.is_outdoor(rx_pos):
                    break
            result = tracer.trace_outdoor(tx_pos, rx_pos)
            lines = lines + OutdoorResultToLines(result, tx_pos, rx_pos)
        window.line_sets = lines
        window.load_obj_to_scene(POZNAN_OBJ_PATH)
        # window.run()